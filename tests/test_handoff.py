"""The handoff runtime: kip running under an agent instead of an API key.

These tests stand in for the agent. Where a real session would have the model
read `pending.jsonl` and append to `responses.jsonl`, the test writes the answer
directly — the protocol is a file contract, so a test can hold up either end.
"""

from __future__ import annotations

import json

import pytest

from kip.handoff import (
    HandoffClient,
    HandoffInvalid,
    HandoffPending,
    call_id,
    read_responses,
    write_answer,
)

SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": "string"}},
    "required": ["answer"],
    "additionalProperties": False,
}


def _ask(client: HandoffClient, user: str = "u"):
    return client.complete_json(
        system="s", user=user, schema=SCHEMA, model="m", add_thinking=False
    )


def test_an_unanswered_call_stops_the_run_and_records_the_question(tmp_path):
    client = HandoffClient(root=tmp_path)
    with pytest.raises(HandoffPending) as caught:
        _ask(client)

    request = caught.value.request
    assert request["system"] == "s"
    assert request["schema"] == SCHEMA
    written = [json.loads(l) for l in client.pending_path.read_text().splitlines()]
    assert [r["call_id"] for r in written] == [request["call_id"]]


def test_an_answered_call_is_served_from_disk(tmp_path):
    client = HandoffClient(root=tmp_path)
    with pytest.raises(HandoffPending) as caught:
        _ask(client)
    write_answer(tmp_path, caught.value.request["call_id"], {"answer": "42"})

    # A fresh client, as a re-invocation of the CLI would build.
    assert _ask(HandoffClient(root=tmp_path)) == {"answer": "42"}


def test_the_same_question_keeps_the_same_id_across_invocations(tmp_path):
    """What makes the protocol resumable: unchanged work must re-ask identically."""
    first = HandoffClient(root=tmp_path)
    with pytest.raises(HandoffPending) as a:
        _ask(first)
    second = HandoffClient(root=tmp_path)
    with pytest.raises(HandoffPending) as b:
        _ask(second)
    assert a.value.request["call_id"] == b.value.request["call_id"]
    # And recorded once, not once per attempt.
    assert len(first.pending_path.read_text().splitlines()) == 1


def test_a_changed_prompt_is_a_different_question(tmp_path):
    """An answer must not silently attach to a question it did not answer."""
    client = HandoffClient(root=tmp_path)
    with pytest.raises(HandoffPending) as a:
        _ask(client, user="first")
    write_answer(tmp_path, a.value.request["call_id"], {"answer": "42"})

    with pytest.raises(HandoffPending) as b:
        _ask(HandoffClient(root=tmp_path), user="second")
    assert b.value.request["call_id"] != a.value.request["call_id"]


def test_an_answer_of_the_wrong_shape_is_rejected_where_it_is_supplied(tmp_path):
    """The SDK gets schema enforcement from the API and the scripted client
    checks explicitly. A hand-written answer has neither, so it is checked here
    -- otherwise a wrong shape surfaces passes later, far from its cause. That
    is not hypothetical: assertions supplied as bare strings once passed
    unchecked and crashed the audit two stages downstream.
    """
    client = HandoffClient(root=tmp_path)
    with pytest.raises(HandoffPending) as caught:
        _ask(client)
    write_answer(tmp_path, caught.value.request["call_id"], {"wrong_key": "42"})

    with pytest.raises(HandoffInvalid) as bad:
        _ask(HandoffClient(root=tmp_path))
    assert "response[" in str(bad.value)


def test_the_pending_signal_survives_a_broad_except_handler():
    """Several passes wrap their model call in `except Exception: report and
    continue`, so that one bad item cannot abort a stage that already produced
    good ones. Correct for a failure, wrong for a pending call: caught there,
    pass 3 reported a failure, wrote an empty artifact, checkpointed the stage
    as done, and the answer supplied afterwards was never read.
    """
    assert not issubclass(HandoffPending, Exception)
    assert not issubclass(HandoffInvalid, Exception)
    with pytest.raises(HandoffPending):
        try:
            raise HandoffPending({"call_id": "x"})
        except Exception:  # noqa: BLE001 - the point of the test
            pytest.fail("a broad handler swallowed the handoff signal")


def test_a_malformed_line_in_the_answers_file_is_skipped_not_fatal(tmp_path):
    """The agent writes this file by hand. Losing a run to one bad line would be
    a poor trade when the next invocation simply re-asks the unanswered call.
    """
    path = tmp_path / "responses.jsonl"
    path.write_text('{"call_id": "a", "response": {"answer": "ok"}}\n{not json\n')
    assert read_responses(path) == {"a": {"answer": "ok"}}


def test_call_id_ignores_key_order_in_the_schema(tmp_path):
    """An equivalent schema built in a different order is the same question."""
    a = call_id(system="s", user="u", model="m",
                schema={"type": "object", "properties": {"x": {}, "y": {}}})
    b = call_id(system="s", user="u", model="m",
                schema={"properties": {"y": {}, "x": {}}, "type": "object"})
    assert a == b
