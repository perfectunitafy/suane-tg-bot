import logging
from aiogram import Router, F, types
from bot.whitelist import ALLOWED_CHATS

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.new_chat_members)
async def handle_new_chat_members(message: types.Message):
    # Логируем все обновления в этой ветке, чтобы увидеть, что происходит
    logger.info(f"DEBUG: Получено событие new_chat_members: {message}")
    
    # Проверяем, добавили ли бота
    bot_id = message.bot.id
    if any(member.id == bot_id for member in message.new_chat_members):
        logger.info(f"DEBUG: Бот добавлен в чат {message.chat.id}")
        if message.chat.id not in ALLOWED_CHATS:
            logger.info(f"DEBUG: Чат {message.chat.id} не разрешен, выхожу.")
            try:
                await message.answer("Этот чат не находится в списке разрешенных. Выхожу.")
                await message.bot.leave_chat(message.chat.id)
            except Exception as e:
                logger.error(f"DEBUG: Ошибка при выходе: {e}")
            return

@router.message(F.new_chat_members | F.left_chat_member | F.new_chat_title | F.new_chat_photo | F.delete_chat_photo | F.pinned_message)
async def delete_system_messages(message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass
