
from app.models.user import User

def test_create_user():
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        first_name="John",
        last_name="Doe",
    )

    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_password"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.id is None

def test_user_preferred_language():
    user = User(
        email="test@example.com",
        password_hash="hashed",
        first_name="Test",
        last_name="User",
        preferred_language="sv",
    )

    assert user.preferred_language == "sv"
    
def test_user_phone():
    user = User(
        email="worker@example.com",
        password_hash="hashed_password",
        first_name="Maria",
        last_name="Santos",
        phone="+639123456789",
    )

    assert user.phone == "+639123456789"


def test_user_default_values():
    user = User(
        email="test@example.com",
        password_hash="hashed_password",
        first_name="John",
        last_name="Doe",
    )

    assert user.is_active is None
    assert user.created_at is None
