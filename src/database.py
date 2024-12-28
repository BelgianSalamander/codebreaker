import asyncio
import aiosqlite
import getpass
import os


connection = None


async def connect():
    global connection
    connection = await aiosqlite.connect(
        database = 'codebreaker.db'
    )

async def fetch_one(query, *params):
    cursor = await connection.cursor()
    cursor.row_factory = aiosqlite.Row
    
    await cursor.execute(query, params)
    return await cursor.fetchone()

async def fetch_all(query, *params):
    cursor = await connection.cursor()
    cursor.row_factory = aiosqlite.Row

    await cursor.execute(query, params)
    return await cursor.fetchall()

loop = asyncio.get_event_loop()
loop.run_until_complete(connect())
