import sqlite3 as sq
from all_kyes import bot, dp, storage
from aiogram.types import ReplyKeyboardMarkup

base = sq.connect('task.bd')
cur = base.cursor()

def sql_start():
    global base, cur
    if base:
        print('Data base connect!')
        base.execute('CREATE TABLE IF NOT EXISTS task(id INTEGER PRIMARY KEY AUTOINCREMENT, img TEXT, '
                     'type TEXT, answer TEXT)')
#        base.execute('DELETE FROM task')
        base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO task (type, img, answer) VALUES(?, ?, ?)', tuple(data.values()))
        base.commit()

async def sql_check_all(message):
    for ret in cur.execute('SELECT * FROM task').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'Тип: {ret[2]}\nОтвет: {ret[-1]}')
        await bot.send_message(message.from_user.id, '➖➖➖➖➖')


async def sql_check_all_task_with_type(message, answer):
    for ret in cur.execute('SELECT * FROM task WHERE type == ?', (answer, )).fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'Тип: {ret[2]}\nОтвет: {ret[-1]}')
        await bot.send_message(message.from_user.id, '➖➖➖➖➖')

async def sql_read():
    return cur.execute('SELECT * FROM task').fetchall()

async def sql_read_with_type(data):
    return cur.execute('SELECT * FROM task WHERE type == ?', (data, )).fetchall()

async def sql_delete_command(base, cur, data):
    cur.execute('DELETE FROM task WHERE id == ?', (data, ))
    base.commit()

async def first_mode_type_exercise(message, data):
    global true_answer
    for ret in cur.execute('SELECT * FROM task WHERE type == ? ORDER BY RANDOM() LIMIT 1', (data, )).fetchall():
        await bot.send_photo(message.from_user.id, ret[1])
        true_answer = str(ret[3])
    return true_answer



async def second_mode_type_exercise(message, data):
    global true_answer_second
    for ret in cur.execute('SELECT * FROM task WHERE type == ? ORDER BY RANDOM() LIMIT 1', (data, )).fetchall():
        await bot.send_photo(message.from_user.id, ret[1], reply_markup=ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True).add('Закончить'))
        true_answer_second = str(ret[3])
    return true_answer_second

