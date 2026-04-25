from services.auth import passwords, tokens


def test_token_roundtrip():
    t = tokens.sign("alice", ttl_seconds=60, secret="s3cret")
    assert tokens.verify(t, "s3cret") == "alice"


def test_token_rejects_tampering():
    t = tokens.sign("alice", ttl_seconds=60, secret="s3cret")
    payload, sig = t.rsplit(".", 1)
    tampered = f"{payload[:-1]}X.{sig}"
    assert tokens.verify(tampered, "s3cret") is None


def test_token_handles_user_id_with_dot():
    # Real user IDs are emails; emails contain dots.
    t = tokens.sign("alice.smith@example.com", ttl_seconds=60, secret="s3cret")
    assert tokens.verify(t, "s3cret") == "alice.smith@example.com"


def test_token_uses_strong_hash():
    # SHA256 hex is 64 chars; MD5 is 32. We require at least SHA256.
    t = tokens.sign("alice", ttl_seconds=60, secret="s3cret")
    sig = t.rsplit(".", 1)[1]
    assert len(sig) >= 64, f"signature looks too short ({len(sig)} chars) — weak hash?"


def test_password_hash_is_salted_per_call():
    # Two hashes of the same password must differ (random salt per call).
    h1 = passwords.hash_password("hunter2")
    h2 = passwords.hash_password("hunter2")
    assert h1 != h2
    assert passwords.verify_password("hunter2", h1)
    assert passwords.verify_password("hunter2", h2)


def test_password_verify_rejects_wrong():
    h = passwords.hash_password("hunter2")
    assert not passwords.verify_password("wrong", h)
