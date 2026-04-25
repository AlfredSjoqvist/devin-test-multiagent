import threading

import pytest

from services.orders.inventory import Inventory, OutOfStock
from services.orders.pagination import paginate


def test_decrement_basic():
    inv = Inventory()
    inv.set_stock("sku-1", 10)
    assert inv.decrement("sku-1", 3) == 7


def test_decrement_raises_when_insufficient():
    inv = Inventory()
    inv.set_stock("sku-1", 2)
    with pytest.raises(OutOfStock):
        inv.decrement("sku-1", 5)


def test_decrement_is_threadsafe():
    inv = Inventory()
    inv.set_stock("sku-1", 100)

    def worker():
        for _ in range(10):
            try:
                inv.decrement("sku-1", 1)
            except OutOfStock:
                pass

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # 10 threads x 10 decrements = 100 total. Stock should be exactly 0.
    assert inv.get_stock("sku-1") == 0


def test_restock_rejects_negative():
    inv = Inventory()
    inv.set_stock("sku-1", 5)
    with pytest.raises(ValueError):
        inv.restock("sku-1", -3)


def test_paginate_first_page():
    items = list(range(25))
    page = paginate(items, page=1, per_page=10)
    assert page["items"] == list(range(10))
    assert page["has_next"] is True


def test_paginate_last_page():
    items = list(range(25))
    page = paginate(items, page=3, per_page=10)
    assert page["items"] == [20, 21, 22, 23, 24]
    assert page["has_next"] is False
