from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Суанэ на связи.")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Я умею: /ban, /mute, /unmute. Общайся со мной через упоминание 'Суанэ' или реплай.")
