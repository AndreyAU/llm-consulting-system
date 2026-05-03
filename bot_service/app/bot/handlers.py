from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.core.jwt import decode_and_validate
from app.infra.redis import get_redis
from app.tasks.llm_tasks import llm_request

router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Это бот с доступом к большой языковой модели по JWT-токену.\n"
        "Сначала отправьте токен командой: /token <JWT>\n"
        "Потом просто напишите вопрос, и я передам его в LLM через очередь RabbitMQ."
    )


@router.message(Command("token"))
async def set_token(message: Message):
    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Используй: /token <JWT>")
        return

    token = parts[1]
    user_id = message.from_user.id

    redis = get_redis()
    await redis.set(f"token:{user_id}", token)

    await message.answer("Токен сохранён ✅")


@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id

    redis = get_redis()
    token = await redis.get(f"token:{user_id}")

    if not token:
        await message.answer("Нет токена. Отправь /token <JWT>")
        return

    try:
        decode_and_validate(token)
    except Exception:
        await message.answer("Неверный или просроченный токен")
        return

    llm_request.delay(message.chat.id, message.text)

    await message.answer("Запрос принят, ожидайте ответ...")
