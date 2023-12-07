import sqlite3 as sq
from all_kyes import bot, dp, storage
from aiogram.types import ReplyKeyboardRemove

full_task_base = sq.connect('full_task.bd')
ft_cur = full_task_base.cursor()

def ft_sql_start():
    global full_task_base, ft_cur
    if full_task_base:
        print('Data base to tasks connect!')
        full_task_base.execute('CREATE TABLE IF NOT EXISTS full_tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, img TEXT, '
                               'answer TEXT)')
#        full_task_base.execute('DELETE FROM task')
        full_task_base.commit()


async def sql_add_command_fulltask(state):
    async with state.proxy() as data:
        ft_cur.execute('INSERT INTO full_tasks (img, answer) VALUES(?, ?)', tuple(data.values()))
        full_task_base.commit()

async def sql_check_all_fulltask(message):
    for ret in ft_cur.execute('SELECT * FROM full_tasks').fetchall():
        await bot.send_photo(message.from_user.id, ret[1], f'Ответ: {ret[-1]}')
        await bot.send_message(message.from_user.id, '➖➖➖➖➖')


def check_full_task():
    ft_cur.execute('SELECT COUNT(*) FROM full_tasks')
    count = ft_cur.fetchone()[0]
    return count > 0

#print(check_full_task())

async def clean_fulltask():
    ft_cur.execute('DELETE FROM full_tasks')

async def third_mode_type_exercise(message, data):
    global true_answer
    for ret in ft_cur.execute('SELECT * FROM full_tasks LIMIT 1 OFFSET ?', (data-1, )).fetchall():#, (data, )
        await bot.send_photo(message.from_user.id, ret[1], reply_markup=ReplyKeyboardRemove())
        true_answer = str(ret[-1])
    return true_answer