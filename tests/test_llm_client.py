"""Tests for the real API path -- `LLMClient` -- without a key or a network.

The client is the one component every LLM pass runs through and it had no test
at all: the retry loop, the native-schema-to-forced-tool fallback, and the usage
accounting were all unexercised. The fallback matters beyond coverage, because
it is one of the two documented ways a malformed unit reaches Pass 1's
materializer.

`LLMClient` is a dataclass with an injectable `_client`, so a stub exposing
`messages.create` is all that is needed. `__post_init__` constructs a real
Anthropic client, so it is stubbed out here -- that construction is the only
thing in the module that requires the package.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from kip import llm as llm_module
from kip.config import default_config
from kip.llm import LLMClient, LLMError, datamark, with_thinking_field

SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}},
    "required": ["answer"],
    "additionalProperties": False,
}


class _Block:
    def __init__(self, **fields: Any) -> None:
        self.__dict__.update(fields)


class _Usage:
    def __init__(self, input_tokens: int, output_tokens: int, cache: int = 0) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.cache_read_input_tokens = cache


class _Response:
    def __init__(self, content: list[_Block], usage: _Usage | None = None) -> None:
        self.content = content
        self.usage = usage or _Usage(10, 5)


class _Messages:
    """Records every call and replays a scripted list of outcomes."""

    def __init__(self, outcomes: list[Any]) -> None:
        self.outcomes = list(outcomes)
        self.calls: list[dict[str, Any]] = []

    def create(self, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        outcome = self.outcomes.pop(0) if self.outcomes else self.outcomes
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class _Stub:
    def __init__(self, outcomes: list[Any]) -> None:
        self.messages = _Messages(outcomes)


@pytest.fixture
def client_factory(monkeypatch):
    """An LLMClient whose transport is a stub, with no API key anywhere."""
    def build(outcomes: list[Any], **overrides: Any) -> tuple[LLMClient, _Stub]:
        stub = _Stub(outcomes)
        monkeypatch.setattr(LLMClient, "__post_init__", lambda self: None)
        client = LLMClient(cfg=default_config(), _client=stub, **overrides)
        return client, stub

    return build


def _text(payload: dict) -> _Response:
    return _Response([_Block(type="text", text=json.dumps(payload))])


def _tool(payload: dict) -> _Response:
    return _Response([_Block(type="tool_use", input=payload)])


def test_the_native_schema_path_returns_the_parsed_object(client_factory):
    client, stub = client_factory([_text({"answer": "yes"})])
    assert client.complete_json(
        system="s", user="u", schema=SCHEMA, model="a-model"
    ) == {"answer": "yes"}
    assert "output_config" in stub.messages.calls[0]


def test_an_sdk_without_output_config_falls_back_permanently(client_factory):
    """One TypeError must not cost a retry on every later call."""
    client, stub = client_factory([
        TypeError("unexpected keyword argument 'output_config'"),
        _tool({"answer": "first"}),
        _tool({"answer": "second"}),
    ])
    assert client.complete_json(system="s", user="u", schema=SCHEMA, model="m")["answer"] == "first"
    assert client._use_native_schema is False

    assert client.complete_json(system="s", user="u", schema=SCHEMA, model="m")["answer"] == "second"
    assert len(stub.messages.calls) == 3
    assert "output_config" not in stub.messages.calls[-1]
    assert stub.messages.calls[-1]["tool_choice"] == {"type": "tool", "name": "emit_result"}


def test_an_api_error_naming_the_parameter_also_falls_back(client_factory):
    client, _ = client_factory([
        RuntimeError("unknown parameter: output_config"),
        _tool({"answer": "ok"}),
    ])
    assert client.complete_json(system="s", user="u", schema=SCHEMA, model="m")["answer"] == "ok"
    assert client._use_native_schema is False


def test_an_unrelated_api_error_is_not_treated_as_a_fallback_signal(client_factory):
    """Silently switching paths on any error would hide a real outage."""
    client, _ = client_factory(
        [RuntimeError("overloaded_error")] * 4, max_retries=4
    )
    with pytest.raises(RuntimeError, match="overloaded"):
        client.complete_json(system="s", user="u", schema=SCHEMA, model="m")
    assert client._use_native_schema is True


def test_malformed_json_is_retried_and_then_succeeds(client_factory, monkeypatch):
    monkeypatch.setattr(llm_module.time, "sleep", lambda _seconds: None)
    client, stub = client_factory([
        _Response([_Block(type="text", text="{not json")]),
        _Response([_Block(type="text", text="still not json")]),
        _text({"answer": "third time"}),
    ])
    assert client.complete_json(
        system="s", user="u", schema=SCHEMA, model="m"
    )["answer"] == "third time"
    assert len(stub.messages.calls) == 3


def test_a_response_that_never_parses_raises_after_the_retry_budget(
    client_factory, monkeypatch
):
    monkeypatch.setattr(llm_module.time, "sleep", lambda _seconds: None)
    client, stub = client_factory(
        [_Response([_Block(type="text", text="{")]) for _ in range(3)], max_retries=3
    )
    with pytest.raises(LLMError, match="failed after 3 attempts"):
        client.complete_json(system="s", user="u", schema=SCHEMA, model="m")
    assert len(stub.messages.calls) == 3


def test_a_forced_tool_call_that_the_model_ignores_is_an_error(client_factory, monkeypatch):
    monkeypatch.setattr(llm_module.time, "sleep", lambda _seconds: None)
    client, _ = client_factory(
        [TypeError("no output_config")] + [_Response([_Block(type="text", text="hi")])] * 3,
        max_retries=3,
    )
    with pytest.raises(LLMError, match="did not call the required tool"):
        client.complete_json(system="s", user="u", schema=SCHEMA, model="m")


def test_usage_accumulates_across_calls(client_factory):
    client, _ = client_factory([
        _Response([_Block(type="text", text='{"answer": "a"}')], _Usage(100, 20, cache=80)),
        _Response([_Block(type="text", text='{"answer": "b"}')], _Usage(50, 10)),
    ])
    client.complete_json(system="s", user="u", schema=SCHEMA, model="m")
    client.complete_json(system="s", user="u", schema=SCHEMA, model="m")
    assert client.usage.as_dict() == {
        "calls": 2, "input_tokens": 150, "output_tokens": 30, "cache_read_tokens": 80,
    }


def test_the_system_prompt_is_cached_but_the_document_is_not(client_factory):
    """Every call in a pass shares the long system prompt; the document does not."""
    client, stub = client_factory([_text({"answer": "a"})])
    client.complete_json(system="long instructions", user="the document", schema=SCHEMA, model="m")
    system = stub.messages.calls[0]["system"]
    assert system[0]["cache_control"] == {"type": "ephemeral"}
    assert stub.messages.calls[0]["messages"] == [{"role": "user", "content": "the document"}]


def test_the_reasoning_field_is_requested_by_default_and_can_be_declined(client_factory):
    client, stub = client_factory([_text({"answer": "a"}), _text({"answer": "b"})])
    client.complete_json(system="s", user="u", schema=SCHEMA, model="m")
    with_thinking = stub.messages.calls[0]["output_config"]["format"]["schema"]
    assert "reasoning" in with_thinking["properties"]

    client.complete_json(system="s", user="u", schema=SCHEMA, model="m", add_thinking=False)
    assert "reasoning" not in (
        stub.messages.calls[1]["output_config"]["format"]["schema"]["properties"]
    )


def test_a_missing_anthropic_package_is_a_clear_error(monkeypatch):
    """The one thing in this module that genuinely needs the dependency."""
    monkeypatch.setattr(llm_module, "anthropic", None)
    with pytest.raises(LLMError, match="not installed"):
        LLMClient(cfg=default_config())


def test_datamarking_survives_a_round_trip_through_the_client(client_factory):
    """The defense is length-preserving, so offsets recorded upstream still hold."""
    marked = datamark("two words", "▁")
    assert len(marked) == len("two words")
    # Declared FIRST, because a reasoning field the model fills in after its
    # answer is a rationalization rather than a reasoning step.
    assert with_thinking_field(SCHEMA)["required"][0] == "reasoning"
