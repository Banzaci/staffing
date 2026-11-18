
import uuid

from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token, decode_access_token


def test_password_hashing():
    password = "SecureTestPassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_access_token():
    user_id = uuid.uuid4()

    token = create_access_token(user_id)

    assert decode_access_token(token) == user_id


def test_invalid_token():
    assert decode_access_token("invalid-token") is None
