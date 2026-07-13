import asyncpg
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Глобальный пул для переиспользования
pool: Optional[asyncpg.Pool] = None

async def get_pool() -> asyncpg.Pool:
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(DATABASE_URL)
    return pool

async def init_db():
    p = await get_pool()
    async with p.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS warns (
                user_id BIGINT,
                chat_id BIGINT,
                count INT DEFAULT 0,
                last_warn_date TIMESTAMP DEFAULT NOW(),
                PRIMARY KEY (user_id, chat_id)
            );
            CREATE TABLE IF NOT EXISTS history (
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                chat_id BIGINT,
                text TEXT,
                timestamp TIMESTAMP DEFAULT NOW()
            );
        ''')

async def get_warns(user_id: int, chat_id: int):
    p = await get_pool()
    row = await p.fetchrow('SELECT count FROM warns WHERE user_id = $1 AND chat_id = $2', user_id, chat_id)
    return row['count'] if row else 0

async def add_warn(user_id: int, chat_id: int):
    p = await get_pool()
    await p.execute('''
        INSERT INTO warns (user_id, chat_id, count, last_warn_date)
        VALUES ($1, $2, 1, NOW())
        ON CONFLICT (user_id, chat_id) 
        DO UPDATE SET count = warns.count + 1, last_warn_date = NOW()
    ''', user_id, chat_id)

async def reset_warns(user_id: int, chat_id: int):
    p = await get_pool()
    await p.execute('DELETE FROM warns WHERE user_id = $1 AND chat_id = $2', user_id, chat_id)

async def save_message(user_id: int, chat_id: int, text: str):
    p = await get_pool()
    await p.execute('INSERT INTO history (user_id, chat_id, text) VALUES ($1, $2, $3)', user_id, chat_id, text)

async def get_history(chat_id: int, limit: int = 15):
    p = await get_pool()
    rows = await p.fetch('''
        SELECT user_id, text FROM history 
        WHERE chat_id = $1 
        ORDER BY timestamp DESC LIMIT $2
    ''', chat_id, limit)
    return list(reversed(rows))
