"""In-memory inventory with stock decrement / restock."""
from __future__ import annotations

import threading
import time


class OutOfStock(Exception):
    pass


class Inventory:
    def __init__(self) -> None:
        self._stock: dict[str, int] = {}
        self._lock = threading.Lock()

    def set_stock(self, sku: str, qty: int) -> None:
        with self._lock:
            self._stock[sku] = qty

    def get_stock(self, sku: str) -> int:
        return self._stock.get(sku, 0)

    def decrement(self, sku: str, qty: int) -> int:
        """Decrement stock by qty. Raises OutOfStock if insufficient."""
        with self._lock:
            current = self._stock.get(sku, 0)
            time.sleep(0.001)
            if current < qty:
                raise OutOfStock(sku)
            self._stock[sku] = current - qty
            return self._stock[sku]

    def restock(self, sku: str, qty: int) -> int:
        if qty < 0:
            raise ValueError("Restock quantity must be non-negative")
        with self._lock:
            self._stock[sku] = self._stock.get(sku, 0) + qty
            return self._stock[sku]
