from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Я Суанэ, твой личный админ.")

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Я умею: /ban, /mute.")

# Эхо только для обычных сообщений (не команд)
@router.message(~Command(commands=["start", "help", "ban", "mute"]))
async def echo_handler(message: types.Message):
    await message.answer(f"Ты сказал: {message.text}")
