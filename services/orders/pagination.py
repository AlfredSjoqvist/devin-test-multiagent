"""Paginate a list of items.

Pages are 1-indexed: page=1 returns the first `per_page` items.
"""
from __future__ import annotations


def paginate(items: list, page: int, per_page: int) -> dict:
    if page < 1 or per_page < 1:
        raise ValueError("page and per_page must be >= 1")
    start = page * per_page
    end = start + per_page
    return {
        "items": items[start:end],
        "page": page,
        "per_page": per_page,
        "total": len(items),
        "has_next": end < len(items),
    }
