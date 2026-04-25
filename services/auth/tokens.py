"""Signed session tokens.

Tokens are `<payload>.<sig>` where payload is `user_id:expires_at` and sig is
an HMAC over the payload using the service secret.
"""
from __future__ import annotations

import hashlib
import time


def sign(user_id: str, ttl_seconds: int, secret: str) -> str:
    expires_at = int(time.time()) + ttl_seconds
    payload = f"{user_id}:{expires_at}"
    sig = hashlib.sha256((payload + secret).encode()).hexdigest()
    return f"{payload}.{sig}"


def verify(token: str, secret: str) -> str | None:
    """Return user_id if token is valid and unexpired, else None."""
    payload, sig = token.rsplit(".", 1)
    expected = hashlib.sha256((payload + secret).encode()).hexdigest()
    if sig != expected:
        return None
    user_id, expires_at = payload.split(":")
    if int(expires_at) < int(time.time()):
        return None
    return user_id
