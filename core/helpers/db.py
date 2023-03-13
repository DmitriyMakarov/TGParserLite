import asyncio
import datetime
import sqlite3
import os
import aiosqlite

cursor = sqlite3.connect(os.environ['VIRTUAL_ENV'] + '/../' + 'res/db/db.sqlite').cursor()


#Проверяем существует ли user
async def check_user_exist(user_id):
    query = f'SELECT user_id FROM users WHERE user_id="{str(user_id)}"'
    db = await aiosqlite.connect(os.environ['VIRTUAL_ENV'] + '/../' + 'res/db/db.sqlite')
    cursor = await db.execute(query)
    rows = await cursor.fetchone()
    if rows != None:
        for row in await cursor.fetchone():
            return row
    await cursor.close()
    await db.close()


#Добавляем пользователя в бд
async def add_user(user_id):
    query = f'INSERT INTO users (user_id, data_reg) VALUES ("{str(user_id)}","{str(datetime.datetime.today())}")'
    db = await aiosqlite.connect(os.environ['VIRTUAL_ENV'] + '/../' + 'res/dbase/db.sqlite')
    await db.execute(query)
    await db.commit()
    await db.close()


#забираем баланс пользователя из базы
async def get_user_balance(user_id):
    query = f'SELECT balance FROM users WHERE user_id="{str(user_id)}"'
    db = await aiosqlite.connect(os.environ['VIRTUAL_ENV'] + '/../' + 'res/dbase/db.sqlite')
    cursor = await db.execute(query)
    rows = await cursor.fetchone()
    for row in rows:
        return row
    await cursor.close()
    await db.close()


#считаем и устанавливаем баланс
async def set_user_balance(user_id):
    query_get_pays = f'SELECT sum FROM bills WHERE user_id=(SELECT id FROM users WHERE user_id="{str(user_id)}" AND payd=1)'
    query_order_count = f'SELECT count(*) FROM orders WHERE user_id=(SELECT id FROM users WHERE user_id="{str(user_id)}")'
    sum_order = 0
    db = await aiosqlite.connect(os.environ['VIRTUAL_ENV'] + '/../' + 'res/dbase/db.sqlite')
    pays_cursor = await db.execute(query_get_pays)
    for pay in await pays_cursor.fetchall():
        sum_order = sum_order + int(pay[0])
    count_cursor = await db.execute(query_order_count)
    for count in await count_cursor.fetchall():
        count = count[0]
    summ = sum_order - (int(count) * 10)
    query_set_balance = f'UPDATE users SET balance={summ} WHERE user_id="{str(user_id)}"'
    await db.execute(query_set_balance)
    await db.commit()
    await db.close()


