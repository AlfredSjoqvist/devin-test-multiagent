"""Render user-supplied notification templates with a context dict.

Used to render emails like "Hi {name}, your order {order_id} shipped."
The template string is provided by end-users (admins building campaigns),
the context is populated by the system.
"""
from __future__ import annotations


def render(template: str, context: dict) -> str:
    return template.format(**context)
