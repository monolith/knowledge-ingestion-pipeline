"""Test doubles for offline runs: a scripted LLM client that checks its schemas.

Ships inside the package rather than beside the tests because two things need
it and neither can import the other -- `tests/test_pipeline_integration.py` and
`demo/run_demo.py`, which loads by path. Build contract §4.2 says the existing
`FakeClient` is the pattern and it should be extended rather than duplicated;
this module is that shared pattern, and the two callers supply only their canned
payloads.

Why the schema check exists at all: the JSON schemas in `extract`, `assess`,
`candidates`, `route` and `audit` ARE the contract with the live model, and both
fakes used to accept the `schema` argument and ignore it. Renaming
`coarse_stance` to `stance` in `ASSESS_SCHEMA` while `assess._materialize` still
read `raw["coarse_stance"]` left the whole suite green -- the one class of drift
no offline test could otherwise catch, because the model that would have
rejected it is the thing being faked.

`check_schema` covers the subset the pipeline's own schemas use: type, required,
enum, properties, items and additionalProperties. It is deliberately not a
general JSON Schema implementation; a dependency would have to be justified and
the schemas here are simple by design.
"""

from __future__ import annotations

from typing import Any, Callable


class SchemaViolation(AssertionError):
    """A canned response does not satisfy the schema its pass declared."""


_TYPES: dict[str, tuple[type, ...]] = {
    "object": (dict,),
    "array": (list, tuple),
    "string": (str,),
    "integer": (int,),
    "number": (int, float),
    "boolean": (bool,),
}


def check_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    """Raise SchemaViolation when `value` does not satisfy `schema`."""
    expected = schema.get("type")
    if expected:
        allowed = _TYPES.get(expected, ())
        # bool is an int in Python; a schema asking for a number must not accept
        # True, because the API would not.
        if expected in ("integer", "number") and isinstance(value, bool):
            raise SchemaViolation(f"{path}: expected {expected}, got boolean")
        if allowed and not isinstance(value, allowed):
            raise SchemaViolation(f"{path}: expected {expected}, got {type(value).__name__}")

    if "enum" in schema and value not in schema["enum"]:
        raise SchemaViolation(f"{path}: {value!r} is not one of {schema['enum']}")

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                raise SchemaViolation(f"{path}: missing required property {name!r}")
        if schema.get("additionalProperties") is False:
            unknown = sorted(set(value) - set(properties))
            if unknown:
                raise SchemaViolation(f"{path}: undeclared propert(ies) {unknown}")
        for name, item in value.items():
            if name in properties:
                check_schema(item, properties[name], f"{path}.{name}")

    if isinstance(value, (list, tuple)) and "items" in schema:
        for index, item in enumerate(value):
            check_schema(item, schema["items"], f"{path}[{index}]")


def declared_properties(schema: dict[str, Any], *path: str) -> set[str]:
    """Property names declared at `path` inside a schema.

    Used by tests that assert every key a pass READS is a key its schema
    DECLARES -- the direction of drift a canned response cannot reveal on its
    own, because the fake and the consumer can be wrong together.
    """
    node = schema
    for step in path:
        node = node.get("properties", {}).get(step, {})
        if node.get("type") == "array":
            node = node.get("items", {})
    return set(node.get("properties", {}))


class ScriptedClientBase:
    """Dispatches a call to a handler by marker text in the system prompt.

    Both offline clients key off the same markers, so the dispatch lives here
    once: a prompt edit that breaks routing now breaks one place instead of two
    that drift apart. Subclasses implement the `_pass_*` handlers and supply
    canned payloads; everything about validation, counting and dispatch is here.

    Marker text rather than an explicit role argument, because the point is to
    exercise the real pass modules unmodified -- they call `complete_json` with
    nothing identifying the caller except the prompt itself.
    """

    # (marker predicate, call name, handler attribute) in dispatch order.
    MARKERS: tuple[tuple[str, str, str], ...] = (
        ("GRANULARITY", "extract", "_pass_extract"),
        ("completeness", "omission", "_pass_omission"),
        ("retrieval context", "enrich", "_pass_enrich"),
        ("label a cluster", "label", "_pass_label"),
        ("coarse stance", "assess", "_pass_assess"),
        ("proposed knowledge-base operations", "plan", "_pass_plan"),
        ("adversarial auditor", "audit", "_pass_audit"),
    )

    def __init__(self) -> None:
        self.calls: list[str] = []
        self.models: set[str] = set()

    def complete_json(
        self, *, system: str, user: str, schema: dict[str, Any], model: str, **kwargs: Any
    ) -> dict[str, Any]:
        self.models.add(model)
        for marker, name, attribute in self.MARKERS:
            if marker in system:
                handler: Callable[[str], dict[str, Any]] = getattr(self, attribute)
                self.calls.append(name)
                response = handler(user)
                # Checked against the schema the PASS declared, not one the fake
                # keeps privately -- otherwise the fake and the schema can drift
                # together and the check proves nothing.
                check_schema(response, schema, f"${name}")
                return response
        raise AssertionError(f"unscripted call with system prompt: {system[:80]!r}")

    def call_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for name in self.calls:
            counts[name] = counts.get(name, 0) + 1
        return counts
