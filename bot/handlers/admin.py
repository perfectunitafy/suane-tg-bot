from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions

router = Router()

@router.message(Command("ban"))
async def cmd_ban(message: types.Message):
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
    if not message.reply_to_message:
        await message.answer("Ответьте на сообщение для мута.")
        return
    try:
        await message.bot.restrict_chat_member(
            message.chat.id, 
            message.reply_to_message.from_user.id, 
            permissions=ChatPermissions(can_send_messages=False)
        )
        await message.answer(f"Пользователь {message.reply_to_message.from_user.first_name} в муте.")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
