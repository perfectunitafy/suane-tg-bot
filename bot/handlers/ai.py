import asyncio
from aiogram import Router, types, F
from bot.config import client
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text & ~F.text.startswith("/") & (
    (F.reply_to_message.from_user.id == 8890656752) |
    F.text.regexp(r"(?i)суанэ|suane")
))
async def ai_handler(message: types.Message):
    # Проверка, что чат в разрешенных
    from bot.whitelist import ALLOWED_CHATS
    if message.chat.id not in ALLOWED_CHATS:
        return
    try:
        prompt = message.text.lower().replace("суанэ", "").replace("suane", "").strip()
        if not prompt: prompt = message.text
        
        # Используем asyncio.to_thread, чтобы не блокировать event loop
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        await message.reply(response.text)
    except Exception as e:
        logger.error(f"ИИ Ошибка: {e}")
        # Выводим подсказку, если 404
        if "404" in str(e):
            await message.reply("Модель не найдена. Админ, проверь логи!")
        else:
            await message.reply(f"Ошибка: {str(e)[:50]}")
