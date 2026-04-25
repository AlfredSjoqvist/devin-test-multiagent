from services.gateway.router import route


def test_route_auth():
    assert route("/auth/login") == "auth"


def test_route_orders():
    assert route("/orders/123") == "orders"


def test_route_notify():
    assert route("/notify/email") == "notifications"


def test_route_auth_admin_does_not_collide_with_auth():
    # `/auth-admin/*` must route to auth-admin, not auth, even though both
    # share the `/auth` prefix.
    assert route("/auth-admin/users") == "auth-admin"


def test_route_unknown():
    assert route("/nope") is None
