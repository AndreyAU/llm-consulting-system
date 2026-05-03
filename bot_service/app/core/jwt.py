from jose import jwt, JWTError
from app.core.config import settings


def decode_and_validate(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_alg],
        )

        # проверка обязательных полей
        if "sub" not in payload:
            raise ValueError("Token missing 'sub'")

        return payload

    except JWTError as e:
        raise ValueError(f"Invalid token: {str(e)}")
