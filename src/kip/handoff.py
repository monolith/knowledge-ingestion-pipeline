"""In-session LLM transport, for running under an agent instead of an API key.

`LLMClient` calls Anthropic and needs a credential. That is the SDK runtime, and
on a host with no key it cannot run at all — which is why, until now, every test
in this package drove a scripted client and the pipeline had never processed a
real document with a real model.

The CLI runtime removes the credential from the picture. When kip runs inside a
Claude Code session the model is already present: the agent *is* the LLM. So
instead of making a network call, `HandoffClient` writes the request to disk and
stops. The agent answers it, writes the answer back, and re-runs the same
command; completed stages resume from their checkpoints and the answered call is
served from the response file.

    kip run --sources docs/ --mode handoff     # -> writes pending.jsonl, exit 10
    (agent reads the request, writes responses.jsonl)
    kip run --sources docs/ --mode handoff     # -> resumes, next request, exit 10
    ...                                        # -> exit 0 when the run completes

**Call identity is content-addressed.** A request's id is a hash of the system
prompt, the user message, the schema and the model. That is what makes the
protocol resumable: re-running produces byte-identical requests for work already
done, so every answered call is a cache hit and only the frontier advances. It
also means an answer cannot silently attach to the wrong question — change a
prompt and its id changes with it.

**One request per invocation, by design.** The obvious optimisation is to batch:
collect every call a stage needs, answer them together, resume once. It is not
safe here. Pass 2 clusters units and then labels each cluster, and pass 3 judges
pairs the clustering produced — later calls in a stage depend on earlier
answers, so a request set collected up front would be built from stale inputs.
Advancing one call at a time is slower and always correct.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .llm import Usage
from .testing import SchemaViolation, check_schema

PROTOCOL_VERSION = "handoff-1"

#: Exit code meaning "a request is waiting for an answer". Distinct from 1
#: (failure) and 2 (validation error) so a wrapper can tell "not finished yet"
#: from "went wrong".
EXIT_PENDING = 10


class HandoffInvalid(BaseException):
    """An answer was supplied but does not match the schema it answers."""

    def __init__(self, call_id_: str, reason: str) -> None:
        super().__init__(f"answer for {call_id_} does not match its schema: {reason}")
        self.call_id = call_id_
        self.reason = reason


class HandoffPending(BaseException):
    """Raised when a call has no answer yet. Carries the request that needs one.

    Inherits BaseException, not Exception, and that is load-bearing. Several
    passes wrap their model call in `except Exception: report and continue` so
    that one bad item cannot abort a stage that has already produced good ones.
    That is right for a failure and wrong for this: a pending call is not a
    failure, it is "stop here and come back". Caught by those handlers, pass 3
    reported an assessment failure, wrote an empty artifact, checkpointed the
    stage as complete, and the answer supplied afterwards was never read.

    Sitting outside Exception means the signal reaches the CLI intact and no
    pass has to know the handoff runtime exists.
    """

    def __init__(self, request: dict[str, Any]) -> None:
        super().__init__(f"awaiting answer for call {request['call_id']}")
        self.request = request


def call_id(*, system: str, user: str, schema: dict[str, Any], model: str) -> str:
    """Content address for one call.

    Schema is serialized with sorted keys so an equivalent schema built in a
    different order is the same call; the whole point is that a re-run of
    unchanged work produces unchanged ids.
    """
    payload = json.dumps(
        {"v": PROTOCOL_VERSION, "system": system, "user": user, "model": model,
         "schema": schema},
        sort_keys=True, ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass
class HandoffClient:
    """An `LLMClient` that answers from disk instead of from the network.

    Interface-compatible with `LLMClient.complete_json` — the pipeline injects
    one or the other and knows the difference only through the exception.
    """

    root: Path
    #: Answers already supplied, `call_id` -> parsed response object.
    answers: dict[str, Any] = field(default_factory=dict)
    #: Requests seen this invocation, in order, for the operator's benefit.
    seen: list[dict[str, Any]] = field(default_factory=list)
    #: Same type the SDK client reports, so `_finish` does not care which
    #: runtime produced the run. Token counts are not knowable here -- the
    #: agent answering the call is not billed through this process -- so it
    #: stays zeroed rather than being faked.
    usage: Usage = field(default_factory=Usage)
    #: Supplied by the CLI so the size guard applies to this runtime too.
    #: Optional because a caller constructing a bare client for replay has
    #: nothing to check against and no reason to be forced to build a Config.
    cfg: Any = None

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.answers = read_responses(self.responses_path)

    @property
    def pending_path(self) -> Path:
        return self.root / "pending.jsonl"

    @property
    def responses_path(self) -> Path:
        return self.root / "responses.jsonl"

    def complete_json(
        self,
        *,
        system: str,
        user: str,
        schema: dict[str, Any],
        model: str,
        max_tokens: int | None = None,
        cache_system: bool = True,
        add_thinking: bool = True,
    ) -> dict[str, Any]:
        # `add_thinking` is honoured so the request the agent sees is the same
        # shape the API runtime would send, and an answer produced under one
        # runtime is valid under the other.
        from .llm import (
            approx_tokens,
            check_answer_size,
            check_request_size,
            resolve_max_output,
            with_thinking_field,
        )

        if self.cfg is not None:
            check_request_size(system=system, user=user, model=model, cfg=self.cfg)
        max_tokens = resolve_max_output(self.cfg, max_tokens)
        effective = with_thinking_field(schema) if add_thinking else schema
        cid = call_id(system=system, user=user, schema=effective, model=model)

        if cid in self.answers:
            answer = self.answers[cid]
            # Validate here, and here specifically. The SDK runtime gets schema
            # enforcement from the API and the scripted client checks explicitly;
            # a hand-written answer has neither, so an answer of the wrong SHAPE
            # would sail through and fail two passes later, far from its cause.
            # That is exactly what happened first time out: assertions supplied
            # as bare strings passed unchecked and crashed the audit.
            try:
                check_schema(answer, effective, f"response[{cid}]")
            except SchemaViolation as exc:
                raise HandoffInvalid(cid, str(exc)) from None
            # Size, not only shape. The API runtime stops generating at the
            # declared ceiling; nothing stops an agent writing an answer by
            # hand. Unchecked, a run answers past its own budget, validates
            # clean, and truncates the first time it is replayed against the
            # API -- which is what three of the four published demo runs did.
            check_answer_size(
                answer_tokens=approx_tokens(json.dumps(answer, ensure_ascii=False)),
                max_tokens=max_tokens,
                call_id_=cid,
            )
            return answer

        request = {
            "protocol": PROTOCOL_VERSION,
            "call_id": cid,
            "model": model,
            "max_tokens": max_tokens,
            "system": system,
            "user": user,
            "schema": effective,
        }
        self.seen.append(request)
        _append_json(self.pending_path, request)
        raise HandoffPending(request)


def read_responses(path: Path) -> dict[str, Any]:
    """Load answered calls. Tolerant of a partly-written file.

    A malformed trailing line is ignored rather than fatal: the agent writes
    this file by hand, and losing a whole run to one bad line would be a poor
    trade when the next invocation simply re-asks the unanswered call.
    """
    answers: dict[str, Any] = {}
    if not Path(path).exists():
        return answers
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        cid, response = row.get("call_id"), row.get("response")
        if isinstance(cid, str) and isinstance(response, dict):
            answers[cid] = response
    return answers


def _append_json(path: Path, obj: dict[str, Any]) -> None:
    # Deduplicated on call_id: re-running re-asks the same question, and an
    # operator reading pending.jsonl should see one entry per open question
    # rather than one per attempt.
    existing = set()
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                existing.add(json.loads(line).get("call_id"))
            except json.JSONDecodeError:
                continue
    if obj["call_id"] in existing:
        return
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def format_request(request: dict[str, Any]) -> str:
    """Render one open request for a human or an agent to answer."""
    return "\n".join([
        f"call_id : {request['call_id']}",
        f"model   : {request['model']}",
        "",
        "--- SYSTEM " + "-" * 60,
        request["system"],
        "",
        "--- USER " + "-" * 62,
        request["user"],
        "",
        "--- SCHEMA " + "-" * 60,
        json.dumps(request["schema"], indent=2, ensure_ascii=False),
    ])


def write_answer(root: Path, call_id_: str, response: dict[str, Any]) -> None:
    """Record an answer. Used by the agent, and by tests standing in for one."""
    path = Path(root) / "responses.jsonl"
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"call_id": call_id_, "response": response},
                            ensure_ascii=False) + "\n")
