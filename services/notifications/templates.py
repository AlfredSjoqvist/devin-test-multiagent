"""Render user-supplied notification templates with a context dict.

Used to render emails like "Hi {name}, your order {order_id} shipped."
The template string is provided by end-users (admins building campaigns),
the context is populated by the system.
"""
from __future__ import annotations


import re

def render(template: str, context: dict) -> str:
    """Render a template, forbidding attribute access."""
    if "." in template:
        # Simplistic but effective check for {a.b} style attribute access.
        # A full parser would be better, but this is a quick fix.
        raise ValueError("Attribute access is not allowed in templates")
    return template.format(**context)
