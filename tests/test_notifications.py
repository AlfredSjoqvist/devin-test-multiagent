import pytest

from services.notifications.retry import send_with_retry
from services.notifications.templates import render


def test_render_basic():
    assert render("Hi {name}", {"name": "alice"}) == "Hi alice"


def test_render_rejects_attribute_access():
    # Templates come from end-users (campaign admins). They must NOT be able
    # to traverse object attributes via {x.__class__...} format-string tricks.
    template = "{user.__class__.__name__}"
    with pytest.raises(Exception):
        render(template, {"user": "alice"})


def test_retry_returns_value_on_success():
    calls = {"n": 0}

    def fn():
        calls["n"] += 1
        if calls["n"] < 2:
            raise RuntimeError("transient")
        return "ok"

    assert send_with_retry(fn, max_attempts=3) == "ok"


def test_retry_raises_on_persistent_failure():
    # If every attempt fails, the caller MUST see the failure. Returning None
    # silently has caused production incidents.
    def fn():
        raise RuntimeError("permanent")

    with pytest.raises(RuntimeError):
        send_with_retry(fn, max_attempts=3)
