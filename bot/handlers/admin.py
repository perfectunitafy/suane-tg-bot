from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from aiogram.enums import ChatMemberStatus
from datetime import datetime, timedelta

router = Router()

async def is_admin(message: types.Message) -> bool:
    # Проверка, является ли пользователь админом или создателем
    member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.CREATOR]

@router.message(Command("ban"))
async def cmd_ban(message: types.Message):
    if not await is_admin(message):
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
    if not await is_admin(message):
        return
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение для мута.")
        return
    
    args = message.text.split()
    minutes = 0
    if len(args) > 1 and args[1].isdigit():
        minutes = int(args[1])
    
    try:
        until_date = None
        if minutes > 0:
            until_date = datetime.now() + timedelta(minutes=minutes)
        
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
    if not await is_admin(message):
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
