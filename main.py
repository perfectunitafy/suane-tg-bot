import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
import asyncpg
from bot.handlers import commands, ai, admin, system
from bot.whitelist import ALLOWED_CHATS, ALLOWED_USERS

# Middleware для фильтрации чатов
async def whitelist_middleware(handler, event, data):
    # Пытаемся достать объект чата из разных типов событий
    chat = None
    if hasattr(event, 'chat'):
        chat = event.chat
    elif hasattr(event, 'message') and event.message:
        chat = event.message.chat
    elif hasattr(event, 'edited_message') and event.edited_message:
        chat = event.edited_message.chat
    elif hasattr(event, 'callback_query') and event.callback_query:
        chat = event.callback_query.message.chat if event.callback_query.message else None

    if chat:
        # Проверка для личных сообщений
        if chat.type == 'private':
            if event.from_user.id not in ALLOWED_USERS:
                return # Игнорируем всех, кроме админа в личке
        # Проверка для групп/супергрупп
        elif chat.id not in ALLOWED_CHATS:
            # При любом событии в неразрешенной группе - выходим
            try:
                await event.bot.leave_chat(chat.id)
            except:
                pass
            return
            
    return await handler(event, data)

async def main():
    load_dotenv()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    
    # Регистрация глобальных middleware
    dp.update.outer_middleware(whitelist_middleware)
    
    # Регистрация с приоритетом
    dp.include_routers(system.router, commands.router, ai.router, admin.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
