"""Credential resolution: tier precedence, defensive parsing, secret hygiene.

Every test here runs offline. The resolver's whole job is to decide *which*
credential to use, which is a pure function of the environment and a file on
disk -- so none of it needs, or is allowed to need, a network call.
"""

from __future__ import annotations

import json
import time

import pytest

from kip.auth import (
    EXPIRY_SKEW_SECONDS,
    OAUTH_BETA_HEADER,
    Resolution,
    default_credentials_path,
    fingerprint,
    format_status,
    read_claude_code_oauth,
    resolve_auth,
)

TOKEN = "sk-ant-oat01-" + "t" * 80
FUTURE_MS = (time.time() + 86400) * 1000


def write_cred(tmp_path, **overrides):
    block = {
        "accessToken": TOKEN,
        "refreshToken": "sk-ant-ort01-" + "r" * 80,
        "expiresAt": FUTURE_MS,
        "scopes": ["user:inference", "user:profile"],
        "subscriptionType": "max",
        "rateLimitTier": "default_claude_max_20x",
    }
    block.update(overrides)
    path = tmp_path / ".credentials.json"
    path.write_text(json.dumps({"claudeAiOauth": block}), encoding="utf-8")
    return path


# --- Tier precedence ----------------------------------------------------------


def test_api_key_beats_everything(tmp_path):
    r = resolve_auth({"ANTHROPIC_API_KEY": "sk-ant-key",
                      "ANTHROPIC_AUTH_TOKEN": "tok"}, write_cred(tmp_path))
    assert r.tier == "env_api_key"
    assert r.client_kwargs == {"api_key": "sk-ant-key"}


def test_api_key_carries_no_oauth_beta_header(tmp_path):
    """An API key must not be sent with the OAuth beta header."""
    r = resolve_auth({"ANTHROPIC_API_KEY": "sk-ant-key"}, write_cred(tmp_path))
    assert "default_headers" not in r.client_kwargs


def test_auth_token_beats_claude_code(tmp_path):
    r = resolve_auth({"ANTHROPIC_AUTH_TOKEN": "tok"}, write_cred(tmp_path))
    assert r.tier == "env_auth_token"
    assert r.client_kwargs["default_headers"]["anthropic-beta"] == OAUTH_BETA_HEADER


def test_claude_code_used_when_env_is_empty(tmp_path):
    r = resolve_auth({}, write_cred(tmp_path))
    assert r.tier == "claude_code_oauth"
    assert r.client_kwargs["auth_token"] == TOKEN
    assert r.client_kwargs["default_headers"]["anthropic-beta"] == OAUTH_BETA_HEADER
    assert r.usable is True


def test_blank_env_vars_do_not_shadow_a_real_credential(tmp_path):
    """An exported-but-empty key is a common shell accident, not a credential."""
    r = resolve_auth({"ANTHROPIC_API_KEY": "", "ANTHROPIC_AUTH_TOKEN": "   "},
                     write_cred(tmp_path))
    assert r.tier == "claude_code_oauth"


def test_falls_through_to_sdk_default_when_nothing_is_available(tmp_path):
    r = resolve_auth({}, tmp_path / "absent.json")
    assert r.tier == "sdk_default"
    assert r.client_kwargs == {}
    assert r.usable is False  # honest: only the SDK can tell at call time
    assert r.warnings


# --- Expiry -------------------------------------------------------------------


def test_expired_token_is_not_used(tmp_path):
    path = write_cred(tmp_path, expiresAt=(time.time() - 60) * 1000)
    r = resolve_auth({}, path)
    assert r.tier == "sdk_default"
    assert any("expired" in w for w in r.warnings)


def test_token_inside_the_skew_window_is_treated_as_expired(tmp_path):
    """Refuse a credential that would die mid-pass rather than start on it."""
    path = write_cred(tmp_path, expiresAt=(time.time() + EXPIRY_SKEW_SECONDS - 30) * 1000)
    assert resolve_auth({}, path).tier == "sdk_default"


def test_soon_to_expire_token_is_used_but_warns(tmp_path):
    path = write_cred(tmp_path, expiresAt=(time.time() + 900) * 1000)
    r = resolve_auth({}, path)
    assert r.tier == "claude_code_oauth"
    assert any("expires in" in w for w in r.warnings)


def test_missing_expiry_is_used_but_flagged(tmp_path):
    path = write_cred(tmp_path)
    raw = json.loads(path.read_text())
    del raw["claudeAiOauth"]["expiresAt"]
    path.write_text(json.dumps(raw), encoding="utf-8")
    r = resolve_auth({}, path)
    assert r.tier == "claude_code_oauth"
    assert any("no expiry" in w for w in r.warnings)


def test_missing_inference_scope_warns(tmp_path):
    r = resolve_auth({}, write_cred(tmp_path, scopes=["user:profile"]))
    assert r.tier == "claude_code_oauth"
    assert any("user:inference" in w for w in r.warnings)


def test_rate_limit_sharing_is_surfaced(tmp_path):
    r = resolve_auth({}, write_cred(tmp_path))
    assert any("rate limit" in w for w in r.warnings)


# --- Defensive parsing: another tool's private file ---------------------------


@pytest.mark.parametrize(
    "content",
    [
        "not json at all",
        "[]",                                    # JSON, wrong root type
        "{}",                                    # no claudeAiOauth
        '{"claudeAiOauth": "a string"}',         # wrong block type
        '{"claudeAiOauth": {}}',                 # no accessToken
        '{"claudeAiOauth": {"accessToken": ""}}',    # empty token
        '{"claudeAiOauth": {"accessToken": 12345}}',  # wrong token type
    ],
)
def test_malformed_credential_files_degrade_never_raise(tmp_path, content):
    path = tmp_path / ".credentials.json"
    path.write_text(content, encoding="utf-8")
    assert read_claude_code_oauth(path) is None
    assert resolve_auth({}, path).tier == "sdk_default"   # degrades, does not crash


def test_absent_file_is_not_an_error(tmp_path):
    assert read_claude_code_oauth(tmp_path / "nope.json") is None


def test_unreadable_file_is_not_an_error(tmp_path):
    """A directory where a file is expected is the cheap portable stand-in for
    an unreadable path (chmod tricks do not hold when tests run as root)."""
    path = tmp_path / "creds-dir.json"
    path.mkdir()
    assert read_claude_code_oauth(path) is None


def test_expiry_of_the_wrong_type_is_treated_as_absent(tmp_path):
    r = resolve_auth({}, write_cred(tmp_path, expiresAt="tomorrow"))
    assert r.tier == "claude_code_oauth"
    assert any("no expiry" in w for w in r.warnings)


def test_non_string_scopes_are_dropped_not_fatal(tmp_path):
    cred = read_claude_code_oauth(write_cred(tmp_path, scopes=["user:inference", 7, None]))
    assert cred["scopes"] == ("user:inference",)


# --- Secret hygiene -----------------------------------------------------------


def test_repr_never_contains_the_token(tmp_path):
    r = resolve_auth({}, write_cred(tmp_path))
    assert TOKEN not in repr(r)
    assert TOKEN not in str(r)


def test_status_output_never_contains_the_token(tmp_path):
    for env in ({}, {"ANTHROPIC_API_KEY": TOKEN}, {"ANTHROPIC_AUTH_TOKEN": TOKEN}):
        text = format_status(resolve_auth(env, write_cred(tmp_path)))
        assert TOKEN not in text
        assert TOKEN[:20] not in text


def test_details_carry_a_fingerprint_not_the_secret(tmp_path):
    details = resolve_auth({}, write_cred(tmp_path)).details
    assert details["token_fingerprint"] == fingerprint(TOKEN)
    assert TOKEN not in json.dumps(details)


def test_fingerprint_is_stable_and_discriminating():
    assert fingerprint("a") == fingerprint("a")
    assert fingerprint("a") != fingerprint("b")
    assert len(fingerprint("a")) == 12
    assert "a" not in fingerprint("a" * 50)  # not a prefix of the input


def test_refresh_token_is_never_read_into_the_resolution(tmp_path):
    """The resolver must not even carry the refresh token around.

    Redeeming it would rotate it and log the user's live Claude Code session
    out; the safest guarantee is that this code never holds it.
    """
    path = write_cred(tmp_path)
    refresh = json.loads(path.read_text())["claudeAiOauth"]["refreshToken"]
    cred = read_claude_code_oauth(path)
    r = resolve_auth({}, path)
    assert refresh not in json.dumps(cred)
    assert refresh not in json.dumps({**r.details, **{k: str(v) for k, v in r.client_kwargs.items()}})
    assert not any("refresh" in k for k in cred)


# --- Misc ---------------------------------------------------------------------


def test_default_path_is_overridable_by_env(monkeypatch, tmp_path):
    monkeypatch.setenv("CLAUDE_CODE_CREDENTIALS", str(tmp_path / "x.json"))
    assert default_credentials_path() == tmp_path / "x.json"


def test_default_path_without_override_points_at_claude_code(monkeypatch):
    monkeypatch.delenv("CLAUDE_CODE_CREDENTIALS", raising=False)
    assert default_credentials_path().parts[-2:] == (".claude", ".credentials.json")


def test_resolution_is_frozen():
    r = Resolution(tier="sdk_default", summary="x")
    with pytest.raises(Exception):
        r.tier = "env_api_key"  # type: ignore[misc]
