"""Retry helper with exponential backoff."""
from __future__ import annotations

import time
from typing import Callable, TypeVar

T = TypeVar("T")


def send_with_retry(fn: Callable[[], T], max_attempts: int = 3) -> T | None:
    """Call fn() with up to max_attempts; backoff doubles each attempt.

    Returns fn()'s result on success. Returns None if all attempts fail.
    """
    last_exc = None
    for attempt in range(max_attempts):
        try:
            return fn()
        except Exception as e:
            last_exc = e
            time.sleep(2 ** attempt)
    raise last_exc
