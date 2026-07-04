import asyncio
import logging
from google import genai
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

async def main():
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()

    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        await message.answer("Суанэ на связи. Команды: /ban, /mute [минуты], /unmute")

    @dp.message(Command("ban"))
    async def cmd_ban(message: types.Message):
        if message.reply_to_message:
            await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
            await message.answer("Пользователь забанен.")

    @dp.message(Command("mute"))
    async def cmd_mute(message: types.Message):
        args = message.text.split()
        minutes = int(args[1]) if len(args) > 1 and args[1].isdigit() else 60
        if message.reply_to_message:
            until = datetime.now() + timedelta(minutes=minutes)
            await bot.restrict_chat_member(
                message.chat.id, 
                message.reply_to_message.from_user.id, 
                permissions=ChatPermissions(can_send_messages=False),
                until_date=until
            )
            await message.answer(f"Пользователь в муте на {minutes} минут.")

    @dp.message(Command("unmute"))
    async def cmd_unmute(message: types.Message):
        if message.reply_to_message:
            await bot.restrict_chat_member(
                message.chat.id, 
                message.reply_to_message.from_user.id, 
                permissions=ChatPermissions(can_send_messages=True)
            )
            await message.answer("Пользователь размучен.")

    @dp.message()
    async def ai_handler(message: types.Message):
        if not message.text or message.text.startswith('/'): return
        try:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=message.text)
            await message.reply(response.text)
        except Exception as e:
            await message.answer("Ошибка ИИ.")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
