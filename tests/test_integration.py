"""Cross-service smoke tests."""
from services.auth import passwords, tokens
from services.gateway.router import route
from services.orders.inventory import Inventory


def test_authed_order_flow():
    # 1. user signs up: hash their password
    stored = passwords.hash_password("hunter2")
    assert passwords.verify_password("hunter2", stored)

    # 2. user logs in: receives a token
    token = tokens.sign("user.42@example.com", ttl_seconds=60, secret="srv")

    # 3. gateway routes /orders to the orders service
    assert route("/orders/new") == "orders"

    # 4. authenticated request reaches orders, which decrements stock
    assert tokens.verify(token, "srv") == "user.42@example.com"
    inv = Inventory()
    inv.set_stock("widget", 5)
    assert inv.decrement("widget", 1) == 4
