"""Credential resolution for the Anthropic SDK.

Ingestion-plugin copy. Kept identical to the wiki-graph plugin's `kwg/auth.py`
so both tools authenticate the same way; cross-plugin imports are forbidden.

The point of this module: **an unset ANTHROPIC_API_KEY does not mean there are
no credentials.** The SDK itself resolves an API key, then an auth token, then
an OAuth profile written by `ant auth login`. This module adds one tier the SDK
does not know about -- the Claude Code CLI's own OAuth credential -- so a plugin
running inside a Claude Code session can use the entitlement the user is already
logged in with, without an API key and without installing anything.

Tier order (first match wins):

  1. ANTHROPIC_API_KEY      -- explicit env always wins, including over a profile
  2. ANTHROPIC_AUTH_TOKEN   -- explicit bearer token
  3. Claude Code OAuth      -- ~/.claude/.credentials.json, if present and unexpired
  4. SDK default            -- an `ant auth login` profile, or WIF, or nothing

Two rules this module will not break:

**It never refreshes the token.** The Claude Code credential carries a
`refreshToken`, and redeeming it typically rotates it. If this process redeemed
it, the copy Claude Code holds would become stale and the user's live session
could be logged out -- the `refresh_token_reused` failure mode. Claude Code owns
refreshing; we only ever read. On a 401 the correct response is to re-read the
file (Claude Code may have refreshed it in the meantime) and retry once.

**It never logs the token.** Every value this module returns for display is
either non-secret metadata or a fingerprint. `Resolution.__repr__` is overridden
because a dataclass repr would otherwise print the token into any traceback.

The Claude Code credential file is that tool's private storage, not a published
interface. It is read defensively: any shape surprise degrades to the next tier
rather than raising.
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

# OAuth bearer tokens require this beta header; API keys must not carry it.
OAUTH_BETA_HEADER = "oauth-2025-04-20"

# Treat a token as expired this many seconds early, so a long pass does not
# start on a credential that dies mid-run.
EXPIRY_SKEW_SECONDS = 120

TIERS = ("env_api_key", "env_auth_token", "claude_code_oauth", "sdk_default")


class AuthError(RuntimeError):
    """Raised only when a tier is explicitly selected and cannot be satisfied."""


def default_credentials_path() -> Path:
    """Claude Code's credential file. Overridable for tests and odd installs."""
    override = os.environ.get("CLAUDE_CODE_CREDENTIALS")
    return Path(override) if override else Path.home() / ".claude" / ".credentials.json"


def fingerprint(secret: str) -> str:
    """Stable, non-reversible identifier for a credential.

    Lets `auth status` say "the same token as last run" without ever putting the
    token itself in a log, a terminal, or a traceback.
    """
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()[:12]


@dataclass(frozen=True)
class Resolution:
    """How the client should authenticate, plus non-secret provenance."""

    tier: str
    summary: str
    client_kwargs: dict[str, Any] = field(default_factory=dict, repr=False)
    details: dict[str, Any] = field(default_factory=dict)
    warnings: tuple[str, ...] = ()

    @property
    def usable(self) -> bool:
        """True when we hold a concrete credential.

        `sdk_default` is not usable-by-inspection: whether it works depends on a
        profile on disk that only the SDK can resolve, so we report it honestly
        as unknown rather than guessing.
        """
        return self.tier != "sdk_default"

    def __repr__(self) -> str:  # never let a traceback print the token
        return f"Resolution(tier={self.tier!r}, summary={self.summary!r})"


def read_claude_code_oauth(path: Path | None = None) -> dict[str, Any] | None:
    """Read Claude Code's OAuth credential, or None if unusable.

    Returns None -- never raises -- for every failure mode: file absent,
    unreadable, not JSON, wrong shape, missing token. This is another tool's
    private file; a shape change must degrade to the next tier, not crash a
    pipeline run.
    """
    path = path or default_credentials_path()
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    if not isinstance(raw, dict):
        return None
    block = raw.get("claudeAiOauth")
    if not isinstance(block, dict):
        return None
    token = block.get("accessToken")
    if not isinstance(token, str) or not token:
        return None
    expires_at = block.get("expiresAt")
    return {
        "access_token": token,
        # expiresAt is epoch milliseconds; None when absent rather than a
        # fabricated default, so "unknown expiry" stays distinguishable.
        "expires_at": expires_at / 1000.0 if isinstance(expires_at, (int, float)) else None,
        "scopes": tuple(s for s in block.get("scopes", []) if isinstance(s, str)),
        "subscription_type": block.get("subscriptionType"),
        "rate_limit_tier": block.get("rateLimitTier"),
        "path": str(path),
    }


def _oauth_resolution(cred: dict[str, Any], now: float) -> Resolution | None:
    """Build a Resolution from a Claude Code credential, or None if expired."""
    expires_at = cred["expires_at"]
    if expires_at is not None and expires_at - EXPIRY_SKEW_SECONDS <= now:
        return None

    warnings: list[str] = []
    if "user:inference" not in cred["scopes"]:
        # Observed scope sets include user:inference; if it is missing the call
        # will fail at request time, so say so up front rather than at pass 1.
        warnings.append(
            "the Claude Code token does not list the 'user:inference' scope; "
            "inference calls may be rejected"
        )
    if expires_at is None:
        warnings.append("the Claude Code token has no expiry field; treating it as current")
    else:
        remaining = int(expires_at - now)
        if remaining < 3600:
            warnings.append(
                f"the Claude Code token expires in {remaining // 60} min; "
                "a long run may outlive it (Claude Code refreshes it in place)"
            )
    if cred["rate_limit_tier"]:
        warnings.append(
            "this shares your Claude Code subscription rate limit -- a large run "
            "competes with interactive sessions"
        )

    expiry_text = (
        time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime(expires_at))
        if expires_at is not None
        else "unknown"
    )
    return Resolution(
        tier="claude_code_oauth",
        summary=(
            f"Claude Code OAuth ({cred['subscription_type'] or 'unknown plan'}), "
            f"expires {expiry_text}"
        ),
        client_kwargs={
            "auth_token": cred["access_token"],
            # OAuth bearer tokens are rejected without this beta header.
            "default_headers": {"anthropic-beta": OAUTH_BETA_HEADER},
        },
        details={
            "source": cred["path"],
            "subscription_type": cred["subscription_type"],
            "rate_limit_tier": cred["rate_limit_tier"],
            "scopes": list(cred["scopes"]),
            "expires_at": expiry_text,
            "token_fingerprint": fingerprint(cred["access_token"]),
        },
        warnings=tuple(warnings),
    )


def resolve_auth(
    env: Mapping[str, str] | None = None,
    credentials_path: Path | None = None,
    now: float | None = None,
) -> Resolution:
    """Pick the highest-priority credential available.

    Always returns a Resolution -- `sdk_default` is the honest "we found nothing
    ourselves, let the SDK try" answer, not an error. Callers that need a hard
    failure should check `.usable`.
    """
    env = os.environ if env is None else env
    now = time.time() if now is None else now

    api_key = (env.get("ANTHROPIC_API_KEY") or "").strip()
    if api_key:
        return Resolution(
            tier="env_api_key",
            summary="ANTHROPIC_API_KEY from the environment",
            client_kwargs={"api_key": api_key},
            details={"source": "env:ANTHROPIC_API_KEY",
                     "token_fingerprint": fingerprint(api_key)},
        )

    auth_token = (env.get("ANTHROPIC_AUTH_TOKEN") or "").strip()
    if auth_token:
        return Resolution(
            tier="env_auth_token",
            summary="ANTHROPIC_AUTH_TOKEN from the environment",
            client_kwargs={
                "auth_token": auth_token,
                "default_headers": {"anthropic-beta": OAUTH_BETA_HEADER},
            },
            details={"source": "env:ANTHROPIC_AUTH_TOKEN",
                     "token_fingerprint": fingerprint(auth_token)},
        )

    cred = read_claude_code_oauth(credentials_path)
    if cred is not None:
        resolved = _oauth_resolution(cred, now)
        if resolved is not None:
            return resolved
        expired_note = (
            "the Claude Code credential is present but expired; "
            "Claude Code refreshes it on use -- run any Claude Code command, "
            "or re-run `claude` to log in again"
        )
    else:
        expired_note = None

    warnings = [expired_note] if expired_note else [
        "no ANTHROPIC_API_KEY, no ANTHROPIC_AUTH_TOKEN, and no readable Claude "
        "Code credential; falling through to the SDK's own resolution "
        "(an `ant auth login` profile, if you have one)"
    ]
    return Resolution(
        tier="sdk_default",
        summary="SDK default resolution (ant profile / workload identity / none)",
        client_kwargs={},
        details={"source": "sdk-default"},
        warnings=tuple(warnings),
    )


def format_status(resolution: Resolution) -> str:
    """Human-readable report. Contains no secrets by construction."""
    lines = [
        f"tier     : {resolution.tier}",
        f"resolved : {resolution.summary}",
        f"usable   : {'yes' if resolution.usable else 'unknown (SDK decides at call time)'}",
    ]
    for key, value in resolution.details.items():
        if key == "source":
            continue
        lines.append(f"  {key:<18} {value}")
    if resolution.details.get("source"):
        lines.append(f"  {'source':<18} {resolution.details['source']}")
    for warning in resolution.warnings:
        lines.append(f"warning  : {warning}")
    if not resolution.usable:
        lines.append(
            "hint     : set ANTHROPIC_API_KEY, or log in with Claude Code, "
            "or run `ant auth login`"
        )
    return "\n".join(lines)
