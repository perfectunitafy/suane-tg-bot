import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from datetime import datetime, timedelta
from bot.whitelist import ALLOWED_USERS, ALLOWED_CHATS
from bot.services import db_service

router = Router()
logger = logging.getLogger(__name__)

async def check_permissions(message: types.Message) -> bool:
    if message.from_user.id not in ALLOWED_USERS and message.chat.id not in ALLOWED_CHATS:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return False
    return True

@router.message(Command("ban"))
async def cmd_ban(message: types.Message):
    if not await check_permissions(message):
        return
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение пользователя для бана.")
        return
    try:
        await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
        await message.answer(f"Пользователь {message.reply_to_message.from_user.first_name} забанен.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("mute"))
async def cmd_mute(message: types.Message):
    if not await check_permissions(message):
        return
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение для мута.")
        return
    
    args = message.text.split()
    minutes = int(args[1]) if len(args) > 1 and args[1].isdigit() else 0
    
    try:
        until_date = datetime.now() + timedelta(minutes=minutes) if minutes > 0 else None
        await message.bot.restrict_chat_member(
            message.chat.id, 
            message.reply_to_message.from_user.id, 
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until_date
        )
        msg = f"Пользователь {message.reply_to_message.from_user.first_name} в муте"
        if minutes > 0:
            msg += f" на {minutes} минут."
        else:
            msg += " навсегда."
        await message.answer(msg)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("unmute"))
async def cmd_unmute(message: types.Message):
    if not await check_permissions(message):
        return
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение для снятия мута.")
        return
    try:
        await message.bot.restrict_chat_member(
            message.chat.id, 
            message.reply_to_message.from_user.id, 
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        await message.answer(f"С пользователя {message.reply_to_message.from_user.first_name} сняты ограничения.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

@router.message(Command("warn"))
async def cmd_warn(message: types.Message):
    logger.info("DEBUG: Запущена команда /warn")
    if not await check_permissions(message): 
        logger.info("DEBUG: Отказано в правах")
        return
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение для предупреждения.")
        return
    target = message.reply_to_message.from_user
    logger.info(f"DEBUG: Выполняю add_warn для пользователя {target.id}")
    await db_service.add_warn(target.id, message.chat.id)
    count = await db_service.get_warns(target.id, message.chat.id)
    logger.info(f"DEBUG: Получен новый счетчик: {count}")
    
    msg = f"Пользователь {target.first_name} получил предупреждение ({count}/3)."
    if count >= 3:
        await message.bot.ban_chat_member(message.chat.id, target.id)
        msg = f"Пользователь {target.first_name} забанен за 3 предупреждения."
    elif count == 2:
        await message.bot.restrict_chat_member(message.chat.id, target.id, permissions=ChatPermissions(can_send_messages=False), until_date=datetime.now() + timedelta(hours=24))
        msg = f"Пользователь {target.first_name} получил мут на 24 часа за 2 предупреждения."
    await message.answer(msg)

@router.message(Command("unwarn"))
async def cmd_unwarn(message: types.Message):
    if not await check_permissions(message): return
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение для снятия предупреждений.")
        return
    await db_service.reset_warns(message.reply_to_message.from_user.id, message.chat.id)
    await message.answer(f"Предупреждения с {message.reply_to_message.from_user.first_name} сняты.")
