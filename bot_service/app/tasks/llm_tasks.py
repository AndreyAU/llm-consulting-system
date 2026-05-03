import asyncio

from aiogram import Bot

from app.core.config import settings
from app.infra.celery_app import celery_app
from app.services.openrouter_client import call_openrouter


@celery_app.task(name="llm_request")
def llm_request(tg_chat_id: int, prompt: str) -> str:
    return asyncio.run(_process_llm_request(tg_chat_id, prompt))


async def _process_llm_request(tg_chat_id: int, prompt: str) -> str:
    bot = Bot(token=settings.telegram_bot_token)

    try:
        answer = await call_openrouter(prompt)
        await bot.send_message(chat_id=tg_chat_id, text=answer)
        return answer
    except Exception as e:
        error_message = f"Ошибка при обращении к LLM: {str(e)}"
        await bot.send_message(chat_id=tg_chat_id, text=error_message)
        return error_message
    finally:
        await bot.session.close()
