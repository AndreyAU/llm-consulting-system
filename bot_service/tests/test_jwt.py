from jose import jwt
import pytest

from app.core.jwt import decode_and_validate
from app.core.config import settings


def create_test_token(payload: dict) -> str:
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_alg)


def test_decode_valid_token():
    payload = {
        "sub": "123",
    }

    token = create_test_token(payload)

    decoded = decode_and_validate(token)

    assert decoded["sub"] == "123"


def test_decode_invalid_token():
    token = "invalid.token.value"

    with pytest.raises(ValueError):
        decode_and_validate(token)
