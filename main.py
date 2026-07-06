import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import os
from bot.handlers import commands, ai, admin

async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    
    # Регистрация с приоритетом
    dp.include_routers(commands.router, ai.router, admin.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
