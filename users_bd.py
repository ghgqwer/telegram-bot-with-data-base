import sqlite3 as sq
from all_kyes import bot,dp


users_base = sq.connect('users.bd')
users_cur = users_base.cursor()

#user_id = message.from_user.id
def start_users_bd():
    global users_base, users_cur
    if users_base:
        print('Users base connect!')
        users_base.execute('CREATE TABLE IF NOT EXISTS users (user_id TEXT,'
                           'created_at_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, '
                           'first_mode_time TEXT, first_mode_points TEXT, '
                           'first_mode_full_points TEXT)')
#        users_base.execute('DELETE FROM users')
        users_base.commit()


async def add_user(id, time, points, full_points):
    users_cur.execute('INSERT INTO users (user_id, first_mode_time, first_mode_points, first_mode_full_points)'
                      '  VALUES (?, ?, ?, ?)', (id, time, points, full_points))
    users_base.commit()


async def check_result(message, id):
    results = users_cur.execute('SELECT * FROM users WHERE user_id = ? ORDER BY created_at_time DESC LIMIT 10',
                                (id,)).fetchall()
    return results

async def check_name_users():
    lst = []
    number_of_user = 1
    for users in users_cur.execute('SELECT DISTINCT user_id FROM users').fetchall():
        information_user = await bot.get_chat(users[0])
        if information_user["active_usernames"]:
            lst.append(f'{number_of_user}. @{information_user["active_usernames"][0]}: tg://user?id={users[0]} ')
        else:
            lst.append(f'{number_of_user}. {information_user["first_name"]}: tg://user?id={users[0]} ')
        number_of_user += 1
        #print(k['first_name'])
    return lst