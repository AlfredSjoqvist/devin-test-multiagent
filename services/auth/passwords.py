"""Password hashing.

Stored format: `<salt_hex>$<hash_hex>`.
"""
from __future__ import annotations

import hashlib
import os




def hash_password(password: str) -> str:
    salt = os.urandom(16)
    h = hashlib.sha256(salt + password.encode()).hexdigest()
    return f"{salt.hex()}${h}"


def verify_password(password: str, stored: str) -> bool:
    salt_hex, h = stored.split("$")
    salt = bytes.fromhex(salt_hex)
    candidate = hashlib.sha256(salt + password.encode()).hexdigest()
    return candidate == h
