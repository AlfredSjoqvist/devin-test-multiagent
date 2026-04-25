"""Tiny prefix router that maps a path to a backend service name."""
from __future__ import annotations

ROUTES: list[tuple[str, str]] = [
    ("/auth", "auth"),
    ("/auth-admin", "auth-admin"),
    ("/orders", "orders"),
    ("/notify", "notifications"),
]


def route(path: str) -> str | None:
    """Return the service name for `path`, or None if no route matches."""
    for prefix, service in ROUTES:
        if path.startswith(prefix):
            return service
    return None
