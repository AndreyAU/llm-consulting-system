from types import SimpleNamespace

import pytest
import fakeredis.aioredis
from jose import jwt

from app.bot.handlers import handle_message, set_token
from app.core.config import settings


class FakeMessage:
    def __init__(self, text: str, user_id: int = 123, chat_id: int = 456):
        self.text = text
        self.from_user = SimpleNamespace(id=user_id)
        self.chat = SimpleNamespace(id=chat_id)
        self.answers = []

    async def answer(self, text: str):
        self.answers.append(text)


def make_token(sub: str = "123") -> str:
    return jwt.encode({"sub": sub}, settings.jwt_secret, algorithm=settings.jwt_alg)


@pytest.mark.asyncio
async def test_set_token_saves_token_in_fakeredis(mocker):
    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)

    token = make_token()
    message = FakeMessage(text=f"/token {token}")

    await set_token(message)

    saved_token = await fake_redis.get("token:123")

    assert saved_token == token
    assert message.answers == ["Токен сохранён ✅"]


@pytest.mark.asyncio
async def test_handle_message_without_token_does_not_call_celery(mocker):
    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)

    delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

    message = FakeMessage(text="Привет")

    await handle_message(message)

    delay_mock.assert_not_called()
    assert message.answers == ["Нет токена. Отправь /token <JWT>"]


@pytest.mark.asyncio
async def test_handle_message_with_valid_token_calls_celery(mocker):
    token = make_token()

    fake_redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
    await fake_redis.set("token:123", token)

    mocker.patch("app.bot.handlers.get_redis", return_value=fake_redis)
    delay_mock = mocker.patch("app.bot.handlers.llm_request.delay")

    message = FakeMessage(text="Объясни JWT", user_id=123, chat_id=456)

    await handle_message(message)

    delay_mock.assert_called_once_with(456, "Объясни JWT")
    assert message.answers == ["Запрос принят, ожидайте ответ..."]
