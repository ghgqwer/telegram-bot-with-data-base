import full_task_bd
from all_kyes import bot, dp, storage
import aiogram.dispatcher.filters
import sqlite3 as sq
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bd import *
from full_task_bd import *
from users_bd import *
import requests
from sdamgia import SdamGIA


import random
from timeit import default_timer as timer


sql_start()
ft_sql_start()
start_users_bd()

Count_of_types = 12  #const

# def types_of_ege(Count_of_types):
#     sdamgia = SdamGIA()
#     catalog = sdamgia.get_catalog('math')
#     list_of_types_ege = {}
#     for i in range(Count_of_types+1):
#         list_of_types_ege[catalog[i]['topic_id']] = sdamgia.get_catalog('math')[i]['topic_name']
#     print(list_of_types_ege)
#     return list_of_types_ege
#        #print(sdamgia.get_catalog('math')[i]['topic_name'])
#
# types_of_ege(Count_of_types)




#types_of_ege(Count_of_types)

# sdamgia = SdamGIA()
# list_of_type_ege = {}
# for i in range(Count_of_types):
#     list_of_type_ege[sdamgia.get_catalog('math')[i]['topic_id']] = sdamgia.get_catalog('math')[i]['topic_name']
#
# print(list_of_type_ege)

len_task = 1 #const
correct_answer =['Отлично', 'Превосходно', 'Великолепно', 'Потрясающе', 'Замечательно', 'Правильно', 'Молодец',
                 'Умница', 'Точно', 'Правильный ответ', 'Здорово', 'Браво', 'Фантастика', 'Супер', 'Восхитительно']

incorrect_feedback_words = ['Попробуй еще раз', 'Не совсем верно', 'Неудача', 'Ошибочка', 'Не правильно', 'Не точно',
                  'Почти получилось', 'Неправильный ответ', 'Неправильное решение', 'Неудачная попытка',
                  'Попробуй другой подход', 'Продолжай стараться', 'Неверно', 'Ответ не сходится']


#------------------------------------------------------Клиент----------------------------------------------------------
@dp.message_handler(commands=['start','help'])
@dp.message_handler(Text(['Привет', 'Hi'], ignore_case=True))
async def commands_start(message: types.Message):
    try:
        b1 = KeyboardButton('Погнали')
        start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_kb.add(b1)
        start_ib = InlineKeyboardMarkup().add(
             InlineKeyboardButton(f'Погнали', callback_data=f'Погнали'))
        await bot.send_message(message.from_user.id, '🤖', reply_markup=start_kb)
        await bot.send_photo(message.from_user.id,  photo=types.InputFile('photo/hi_bot.jpg'),
                                          caption= f"Привет, "
                                                     f"@{message.from_user.first_name}"
                                                     f", меня зовут Гиро, и я постараюсь помочь тебе подготовится к "
                                                     f"экзамену по математике, погнали!?",
                                                     reply_markup=InlineKeyboardMarkup().add(
                                                     InlineKeyboardButton(f'Погнали', callback_data=f'Погнали')))
    except:
        await bot.send_message(message.from_user.id, 'Общение с ботом через ЛС')


@dp.message_handler(commands=['menu'])
@dp.callback_query_handler(Text(['Погнали', 'Меню', 'Back_to_menu']))
@dp.message_handler(Text(['Погнали', 'Меню', 'Назад'], ignore_case=True))
async def bot_go(message: types.Message):
    #await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)
    await bot.send_message(message.from_user.id, '🤖', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                one_time_keyboard=True).add(KeyboardButton(f'Первый '
                                                                                                         f'режим'),
                                                                                             KeyboardButton(f'Второй '
                                                                                                            f'режим'),
                                                                                             KeyboardButton(f'Третий '
                                                                                                            f'режим')))
    await bot.send_photo(message.from_user.id, photo=types.InputFile('photo/bot_go.jpg'), caption='У тебя на выбор '
                                                                                                 'есть 3 режима: \n'
                                                               '1. На время - тут тебе предстоит решить полностью всю '
                                                               'первую часть ЕГЭ по профильной математике на время \n'
                                                               '2. Решать определенный тип\n'
                                                               '3. Тест от '
                                                               'преподавателя',
                         reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(f'1',
                                                                                      callback_data='First_mode'),
                                                                 InlineKeyboardButton(f'2',
                                                                                      callback_data='Second_mode'),
                                                                 InlineKeyboardButton(f'3',
                                                                                      callback_data='Third_mode')))


#---------------------Первый режим---------------------
class FSMfirst_mode(StatesGroup):
    Answer = State()
@dp.message_handler(commands=['First_mode'])
@dp.callback_query_handler(Text(['First_mode', 'Первый режим']))
@dp.message_handler(Text('Первый режим', ignore_case=True))
async def First_mode_game(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, '🤖',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
                               KeyboardButton(f'Старт'), KeyboardButton('Назад')))
    await bot.send_message(callback_query.from_user.id,f'В этом режиме тебе предстоит на вермя решить {Count_of_types} задач из '
                                                       f'ЕГЭ по '
                                           'математике на время, постарайся сделать их правильно и как можно '
                                           'быстрее. Чтобы ответить, просто отправь мне сообщение.\n\n '
                                           'Когда будешь готов, намжи кнопку старт',
                           reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(f'Старт',
                                                                                        callback_data='Start_first_mode'),
                                                                   InlineKeyboardButton(f'Назад',
                                                                                        callback_data='Back_to_menu')
                                                                   ))

#len_task
count_of_true_answers = 0
numb_of_type = 1
flag_to_timer = 0
@dp.message_handler(commands=['Start_first_mode'])
@dp.callback_query_handler(Text('Start_first_mode'))
@dp.message_handler(Text('Старт', ignore_case=True))
async def First_mode_game_start(message: types.Message):
    global numb_of_type, true_answer, count_of_true_answers, flag_to_timer, start
    if flag_to_timer == 0:
        start = timer()
    if numb_of_type <= Count_of_types:
        flag_to_timer += 1
        true_answer = await first_mode_type_exercise(message, numb_of_type)
        await FSMfirst_mode.Answer.set()
        numb_of_type += 1
    else:
        end = timer()
        all_time = round(float(end - start), 2)
        await bot.send_message(message.from_user.id, f"Ты закончил, у тебя {count_of_true_answers} "
                                                     f"правильных ответов из {Count_of_types}.\nТы затратил "
                                                     f"{time_result(all_time)}.\n\n"
                                                     f"Узнать все результаты - /result \n"
                                                     f"Хочешь ещё позаниматься?", reply_markup=InlineKeyboardMarkup(

        ).row(InlineKeyboardButton('Погнали!', callback_data='First_mode'),
                                                                   InlineKeyboardButton(f'Назад',
                                                                                        callback_data='Back_to_menu')))
        user_id = message.from_user.id
        await add_user(user_id, time_result(all_time), count_of_true_answers, Count_of_types)
        numb_of_type = 1
        count_of_true_answers = 0
        flag_to_timer = 0


@dp.message_handler(state=FSMfirst_mode)
async def load_answer_first_game_mode(message: types.Message, state: FSMContext):
    global count_of_true_answers
    answer = message.text
    if answer == true_answer:
        count_of_true_answers += 1
        await bot.send_message(message.from_user.id, '👏')
        await bot.send_message(message.from_user.id, text=random.choice(correct_answer))#, f'Отправь мне ответ на это задание'
    else:
        await bot.send_message(message.from_user.id, '😔')
        await bot.send_message(message.from_user.id, text=random.choice(incorrect_feedback_words))
    await state.finish()
    await First_mode_game_start(message)






#-----------------------------------------------------------Второй режим ---------------------------------------------

class FSMsecond_mode(StatesGroup):
    Type_of_task = State()
    Answer = State()
@dp.message_handler(commands=['Second_mode'])
@dp.callback_query_handler(Text(['Second_mode', 'Второй режим']))
@dp.message_handler(Text('Второй режим', ignore_case=True))
async def Second_mode_game(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, '🤖',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
                               KeyboardButton(f'Готов'), KeyboardButton('Назад')))
    await bot.send_message(callback_query.from_user.id,f'В этом режиме ты можешь выбрать задание определенного типа, '
                                                       f'и решать их пока сам не захочешь закончить',
                           reply_markup=InlineKeyboardMarkup().row(InlineKeyboardButton(f'Готов',
                                                                                        callback_data='Start_second_mode'),
                                                                   InlineKeyboardButton(f'Меню',
                                                                                        callback_data='Back_to_menu')
                                                                   ))


@dp.message_handler(commands=['Start_second_mode'])
@dp.callback_query_handler(Text('Start_second_mode'))
@dp.message_handler(Text('Готов', ignore_case=True))
async def Second_mode_type(message: types.Message):
    global Trys, Count_true_ans_second_mode
    Trys = 0
    Count_true_ans_second_mode = 0

    #Создание сообщения с типами
    list_of_type_ege = types_of_ege(Count_of_types)
    message_with_types = ''
    for key, value in list_of_type_ege.items():
        message_with_types += f'{key}. {value}\n'

    #Для количества кнопок, которое меняется в зависимости от количества вариантов
    buttons = []
    for option in list_of_type_ege.keys():
        buttons.append(KeyboardButton(option))
    #print(buttons)
    await bot.send_message(message.from_user.id, f'Какого типа задание будешь решать?\n\n{message_with_types}',
                           reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                               *buttons))
    await FSMsecond_mode.Type_of_task.set()

# @dp.message_handler(commands=['Start_second_mode'])
# @dp.callback_query_handler(Text('Start_second_mode'))
# @dp.message_handler(Text('Готов', ignore_case=True))
# async def Second_mode_type(message: types.Message):
#     global Trys, Count_true_ans_second_mode
#     Trys = 0
#     Count_true_ans_second_mode = 0
#     await bot.send_message(message.from_user.id, 'Какого типа задание будешь решать?',
#                            reply_markup=ReplyKeyboardRemove())
#     await FSMsecond_mode.Type_of_task.set()

@dp.message_handler(state=FSMsecond_mode.Type_of_task)
async def load_type_second_game_mode(message: types.Message, state: FSMContext):
    global answer_type
    answer_type = message.text
    #print(answer_type)
    if answer_type.isdigit() and int(answer_type) <= Count_of_types and int(answer_type) != 0:
        await Send_task_second_mode(message)
    else:
        await bot.send_message(message.from_user.id, 'Такого типа задания не существует',
                               reply_markup=ReplyKeyboardRemove())
        await state.finish()

async def Send_task_second_mode(message: types.Message):
    global true_answer_second_mode
    true_answer_second_mode = await second_mode_type_exercise(message, answer_type)
    await FSMsecond_mode.Answer.set()


@dp.message_handler(state=FSMsecond_mode.Answer)
async def Check_answer_second_mode(message: types.Message, state: FSMContext):
    global count_of_true_answers, true_answer_second_mode, Trys, Count_true_ans_second_mode
    answer = message.text
    if answer == 'Закончить':
        if Trys > 0:
            await bot.send_message(message.from_user.id,
                                   f'Молодец, ты хорошо позанимался. \nУ тебя {Count_true_ans_second_mode} '
                                   f'правильных ответов из {Trys}', reply_markup=ReplyKeyboardMarkup(
                resize_keyboard=True).add('Меню'))
        else:
            await bot.send_message(message.from_user.id, 'В следующий раз постарайся сделать больше заданий', reply_markup=ReplyKeyboardMarkup(
                resize_keyboard=True).add('Меню'))
        await state.finish()
    else:
        Trys += 1
        if answer == true_answer_second_mode:
            Count_true_ans_second_mode += 1
            await bot.send_message(message.from_user.id, '👏')
            await bot.send_message(message.from_user.id, text=random.choice(correct_answer))#, f'Отправь мне ответ на это задание'
        else:
            await bot.send_message(message.from_user.id, '😔')
            await bot.send_message(message.from_user.id, f'{random.choice(incorrect_feedback_words)} \nПравильный '
                                                         f'Ответ: {true_answer_second_mode}')
        await Send_task_second_mode(message)



#---------------------Третий режим---------------------
number_of_attempts = 0
Attempts = 2
lst_of_user_task = []
class FSMthird_mode(StatesGroup):
    Answer = State()
@dp.message_handler(commands=['Third_mode'])
@dp.callback_query_handler(Text(['Third_mode', 'Третий режим']))
@dp.message_handler(Text(['Третий режим', 'Попробовать ещё раз'], ignore_case=True))
async def Third_mode_game(callback_query: types.CallbackQuery):
    count_of_true_answers = 0
    if check_full_task() == False:
        await bot.send_message(callback_query.from_user.id, 'Теста пока нет')
    elif lst_of_user_task.count(f'{callback_query.from_user.id}') >= Attempts:
        await bot.send_message(callback_query.from_user.id, 'У тебя закончились попытки')
    else:
        await bot.send_message(callback_query.from_user.id, '🤖',
                               reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(
                                   KeyboardButton(f'Начать'), KeyboardButton('Назад')))
        await bot.send_message(callback_query.from_user.id, f'В этом режиме тебе предстоит на вермя решить {len_task} '
                                                            f'задач из теста составленного твоим препадователем,'
                                                            f'у тебя всего '
                                                            f'{Attempts - lst_of_user_task.count(f"{callback_query.from_user.id}")}'
                                                            f' попытка(и) удачи!',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Старт',
                                                                                            callback_data='Start_third_mode'),
                                                                       InlineKeyboardButton(f'Назад',
                                                                                            callback_data='Back_to_menu')))

@dp.message_handler(commands=['Start_third_mode'])
@dp.callback_query_handler(Text('Start_third_mode'))
@dp.message_handler(Text('Начать', ignore_case=True))
async def third_mode_game_start(message: types.Message):
    global numb_of_type, true_answer, count_of_true_answers, flag_to_timer, start, number_of_attempts
    if flag_to_timer == 0:
        start = timer()
    if numb_of_type <= len_task and lst_of_user_task.count(f'{message.from_user.id}') < Attempts:
        flag_to_timer += 1
        true_answer = await third_mode_type_exercise(message, numb_of_type)
        await FSMthird_mode.Answer.set()
        numb_of_type += 1
    elif lst_of_user_task.count(f'{message.from_user.id}') >= Attempts:#number_of_attempts >= Attempts or
        await bot.send_message(message.from_user.id, 'У тебя больше не осталось попыток(')
    else:
        end = timer()
        all_time = round(float(end - start), 2)
        number_of_attempts += 1
        lst_of_user_task.append(str(message.from_user.id))

        if lst_of_user_task.count(f'{message.from_user.id}') < Attempts:
            await bot.send_message(message.from_user.id, '✅', reply_markup=ReplyKeyboardMarkup(
                resize_keyboard=True).add('Попробовать ещё раз'))
            await bot.send_message(message.from_user.id, f"Ты закончил, у тебя {count_of_true_answers} "
                                                         f"правильных ответов из {len_task}.\nТы затратил "
                                                         f"{time_result(all_time)}",
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Поробовать еще '
                                                                                                'раз', callback_data='Start_third_mode')))#,
            # reply_markup=ReplyKeyboardRemove()
        else:
            await bot.send_message(message.from_user.id, '✅', reply_markup=ReplyKeyboardMarkup(
                resize_keyboard=True).add('Меню'))
            await bot.send_message(message.from_user.id, f"Ты закончил, у тебя {count_of_true_answers} "
                                                         f"правильных ответов из {len_task}.\nТы затратил "
                                                         f"{time_result(all_time)}",
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton('Меню',
                                                                                                callback_data='Back_to_menu')))
        numb_of_type = 1
        count_of_true_answers = 0
        flag_to_timer = 0



@dp.message_handler(state=FSMthird_mode)
async def load_answer_first_game_mode(message: types.Message, state: FSMContext):
    global count_of_true_answers
    answer = message.text
    if answer == true_answer:
        count_of_true_answers += 1
        await bot.send_message(message.from_user.id, '👏')
        await bot.send_message(message.from_user.id, text=random.choice(correct_answer))#, f'Отправь мне ответ на это задание'
    else:
        await bot.send_message(message.from_user.id, '😔')
        await bot.send_message(message.from_user.id, text=random.choice(incorrect_feedback_words))
    await state.finish()
    await third_mode_game_start(message)



#-------------Узнать результаты-----------------
@dp.message_handler(commands=['result'])
async def result(message: types.Message):
    result = await check_result(message, message.from_user.id)
    string_result = ''
    numb_of_result = 1
    if result:
        for ret in result:
            string_result += f'{numb_of_result}. {ret[3]}/{ret[-1]}  |  ({ret[2]}) \n'
            numb_of_result += 1
        await bot.send_message(message.from_user.id, string_result)
    else:
        await bot.send_message(message.from_user.id, 'Нет результатов')

@dp.message_handler(commands=['check_all_users'])
async def name_users(message: types.Message):
    if message.from_user.id == ID or message.from_user.id == 1143118992:
        users = await check_name_users()
        users = '\n'.join(users)
        await bot.send_message(message.from_user.id, f'Пользователи бота:\n{users}')

@dp.message_handler(commands='check_users')
async def count_users(message: types.Message):
    if message.from_user.id == ID or message.from_user.id == 1143118992:
        users = await check_name_users()
        await bot.send_message(message.from_user.id, f'Количество пользователей бота: {len(users)}')



# if check_result(message, message.from_user.id):
#     await check_result(message, message.from_user.id)
# else:
#     await bot.send_message(message.from_user.id, 'Результатов не найдено')
#-------------------------Админ-----------------------------
ID = None

button_load = KeyboardButton('Загрузить')
button_delete = KeyboardButton('Удалить')
button_all = KeyboardButton('Посмотреть все задания')
button_all_with_type = KeyboardButton('Посмотреть все задания по типу')
button_change_count_type = KeyboardButton('Изменить количество типов задач')
button_full_test = KeyboardButton('Создать полный вариант')
button_check_full_test = KeyboardButton('Посмотреть сущесвующий вариант')
button_del_full_test = KeyboardButton('Удалить вариант')
button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(button_load, button_delete) \
    .add(button_all).add(button_all_with_type).add(button_change_count_type).add(button_full_test).add(
    button_check_full_test).add(button_del_full_test)

class FSMadmin(StatesGroup):
    type = State()
    photo = State()
    answer = State()
@dp.message_handler(commands=['moderator'], is_chat_admin = True)
#@dp.message_handler(commands=['moderator'])  #исправить
async def make_change_commands(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_photo(message.from_user.id,photo=types.InputFile('photo/bot_bd.jpg'), caption='Теперь у вас есть '
                                                                                                'возможность управлять '
                                                                         'базой данных!', reply_markup=button_case_admin)
    await message.delete()

@dp.message_handler(Text('Загрузить', ignore_case=True), state=None)
@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMadmin.type.set()
        await message.reply('Введи тип задание', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                  one_time_keyboard = True).add(
            KeyboardButton('Отмена')))

#Отмена (выход из машинного состояния)
@dp.message_handler(commands='отмена', state='*')
@dp.callback_query_handler(Text('cancel'))
@dp.message_handler(Text('отмена', ignore_case=True), state='*')#, state='*'
async def cansel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok', reply_markup=button_case_admin)


#Ловим ответ от пользователя и вносим в словарь
@dp.message_handler(state=FSMadmin.type)
async def load_photo(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text
    await FSMadmin.next()
    #await message.reply('Введи тип задание')
    await message.reply('Загрузите фото с заданием', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                  one_time_keyboard = True).add(
            KeyboardButton('Отмена')))

# Ловим второй ответ
@dp.message_handler(content_types=['photo'], state=FSMadmin.photo)
async def load_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMadmin.next()
    await message.reply('Введи ответ', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True,
                                                                                  one_time_keyboard = True).add(
            KeyboardButton('Отмена')))

@dp.message_handler(state=FSMadmin.answer)
async def load_answer(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['answer'] = message.text
    await sql_add_command(state)
    await bot.send_message(message.from_user.id, text='Готово', reply_markup=button_case_admin)
    # async with state.proxy() as data:
    #     await message.reply(str(data))
    await state.finish()


#Удалить
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sql_delete_command(base, cur, callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'Готово', show_alert=True)

#---------------------Удалить задание---------------------
class Delete_question(StatesGroup):
    Answer = State()
@dp.message_handler(commands='Delete')
@dp.message_handler(Text('Удалить', ignore_case=True))
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Показать всю базу данных или вывести задания по типу?',
                               reply_markup=InlineKeyboardMarkup().row(
                 InlineKeyboardButton(f'Всю базу данных', callback_data=f'all_sql_to_del'),
                 InlineKeyboardButton(f'По типу', callback_data=f'type_sql_to_del')))

@dp.callback_query_handler(Text('all_sql_to_del'))
async def all_sql_to_del(callback_query: types.CallbackQuery):
    read = await sql_read()
    for ret in read:
        await bot.send_photo(callback_query.from_user.id, ret[1], f'Тип: {ret[2]}\nОтвет: {ret[-1]}',
                             reply_markup=InlineKeyboardMarkup().add(
            InlineKeyboardButton(f'Удалить', callback_data=f'del {ret[0]}')))
        await bot.send_message(callback_query.from_user.id, '➖➖➖➖➖')
        # await bot.send_photo(callback_query.from_user.id, ret[1], f'Тип: {ret[2]}\nОтвет: {ret[-1]}')
        # await bot.send_message(callback_query.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().add(
        #     InlineKeyboardButton(f'Удалить', callback_data=f'del {ret[0]}')))

@dp.callback_query_handler(Text('type_sql_to_del'))
async def what_type_to_del(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, 'Какого типа задания для удаления вывести?')
    await Delete_question.Answer.set()

#Отмена (выход из машинного состояния)
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text('отмена', ignore_case=True), state='*')
async def cansel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok')

@dp.message_handler(state=Delete_question.Answer)
async def state_ask(message: types.Message, state: FSMContext):
    data = message.text
    read = await sql_read_with_type(data)
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[1], f'Тип: {ret[2]}\nОтвет: {ret[-1]}',
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton(f'Удалить', callback_data=f'del {ret[0]}')))
        await bot.send_message(message.from_user.id, '➖➖➖➖')
    await state.finish()



#---------------------Просмотр заданий---------------------
@dp.message_handler(Text('Посмотреть все задания', ignore_case=True))
@dp.message_handler(commands=['Check_all_tasks'])
async def check_type_of_task(message: types.Message):
    await sql_check_all(message)


class State_to_type(StatesGroup):
    Answer = State()
@dp.message_handler(Text('Посмотреть все задания по типу', ignore_case=True))
@dp.message_handler(commands=['Check_all_task_with_type'])
async def cmd_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Какого типа задание вывести?')
    await State_to_type.Answer.set()

#Отмена (выход из машинного состояния)
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text('отмена', ignore_case=True), state='*')
async def cansel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok')

@dp.message_handler(state=State_to_type.Answer)
async def state_ask(message: types.Message, state: FSMContext):
    answer = message.text
    await sql_check_all_task_with_type(message, answer)
    await state.finish()


#---------------------Изменить количество типов---------------------
class State_to_count_of_type_answer(StatesGroup):
    Answer = State()
@dp.message_handler(Text('Изменить количество типов задач', ignore_case=True))
@dp.message_handler(commands=['Change_count_of_types'])
async def change_count_of_types(message: types.Message):
    await bot.send_message(message.from_user.id, 'Сколько типов заданий у нас будет?')
    await State_to_count_of_type_answer.Answer.set()

#Отмена (выход из машинного состояния)
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text('отмена', ignore_case=True), state='*')
async def cansel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok')

@dp.message_handler(state=State_to_count_of_type_answer.Answer)
async def change_count_of_types_ask(message: types.Message, state: FSMContext):
    global Count_of_types
    answer = message.text
    if answer.isdigit() and int(answer) <= all_types_of_ege():
        Count_of_types = int(answer)
        await bot.send_message(message.from_user.id, f'Теперь у нас {Count_of_types} типов(а) заданий')
    else:
        await bot.send_message(message.from_user.id, f'Невозможно установить такое количество заданий')
    await state.finish()

#---------------------Посмотреть существующий вариант---------------------
@dp.message_handler(Text('Посмотреть сущесвующий вариант'))
@dp.message_handler(commands=['check_full_test'])
async def check_full_test(message: types.Message):
    await sql_check_all_fulltask(message)

#---------------------Создать полный вариант---------------------
class FSMfull_test(StatesGroup):
    Len_of_task = State()
    Attempts = State()
    Photo = State()
    Answer = State()
@dp.message_handler(Text(equals='Создать полный вариант', ignore_case=True))
@dp.message_handler(commands=['Create_full_test'])
async def len_full_test(message: types.Message):
    await bot.send_message(message.from_user.id, 'Сколько заданий будет в твоём тесте?')
    await clean_fulltask()
    await FSMfull_test.Len_of_task.set()

#Отмена (выход из машинного состояния)
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text('отмена', ignore_case=True), state='*')
async def cansel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok')

@dp.message_handler(state=FSMfull_test.Len_of_task)
async def process_len_task(message: types.Message, state: FSMContext):
    global len_task, count_of_task
    count_of_task = 0
    len_task = int(message.text)
    if len_task <= 0:
        await bot.send_message(message.from_user.id,f'Тест не может состоять из {len_task} заданий')
        await state.finish()
    else:
        #await state.finish()
        await FSMadmin.next()
        await bot.send_message(message.from_user.id,'Сколько попыток будет на решение варианта')
        await FSMfull_test.Attempts.set()

@dp.message_handler(state=FSMfull_test.Attempts)
async def process_len_task(message: types.Message, state: FSMContext):
    global Attempts
    Attempts = int(message.text)
    #print(Attempts)
    if Attempts <= 0:
        await bot.send_message(message.from_user.id,f'В тесте не может быть {Attempts} попыток')
        await state.finish()
        number_of_attempts = 0
    else:
    #await state.finish()
        await process_len_task(message)

@dp.message_handler(Text('', ignore_case=True), state='*')
async def process_len_task(message: types.Message):
    global number_of_attempts, lst_of_user_task
    if count_of_task < len_task:
        await bot.send_message(message.from_user.id, 'Отправь картнку с заданием')
        await FSMfull_test.Photo.set()
    else:
        await bot.send_message(message.from_user.id, f'Вариант из {len_task} заданий сотавлен!')
        number_of_attempts = 0
        lst_of_user_task = []

#Отмена (выход из машинного состояния)
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text('отмена', ignore_case=True), state='*')
async def cansel_handler(message : types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ok')

@dp.message_handler(content_types=['photo'], state=FSMfull_test.Photo)
async def load_photo_to_full_task(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await FSMadmin.next()
    await message.reply('Отправь ответ')
    await FSMfull_test.Answer.set()

@dp.message_handler(state=FSMfull_test.Answer)
async def load_answer_to_full_task(message: types.Message, state: FSMContext):
    global count_of_task
    async with state.proxy() as data:
        data['Answer'] = message.text
    await bot.send_message(message.from_user.id, 'Готово')
    await sql_add_command_fulltask(state)
    await state.finish()
    count_of_task += 1
    await process_len_task(message)


#---------------------Удалить полный вариант---------------------
@dp.message_handler(Text(equals='Удалить вариант', ignore_case=True))
@dp.message_handler(commands=['Del_all_tasks'])
async def check_type_of_task(message: types.Message):
    await clean_fulltask()
    await bot.send_message(message.from_user.id, 'Готово')

#--------------------------------------------------------------------------------------------------

#-------------------------Прочее-----------------------------

#Перевод float во время
def time_result(k):
    hour = k // 3600 #hour
    k -= hour * 3600
    minut = int(k // 60) #minutes
    k -= 60*minut
    # second = round(float(k),2) #seconds
    second = int(k) #second
    return f'{str(minut)} мин, {str(second)} сек'

# def types_of_ege():
#     url = 'https://ege.sdamgia.ru/newapi/general'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, '
#                       'like Gecko) Chrome/114.0.0.0Mobile Safari/537.36',
#         'Accept - Ranges': 'bytes'
#     }
#     list_of_types_ege = {}
#     response = requests.get(url, headers=headers).json()
#     for data in response['constructor']:
#         if data['type'] == 'short':
#             list_of_types_ege[data['num']] = data['title']
#     return list_of_types_ege


def types_of_ege(Count_of_types, catalog_cache=None):
    if catalog_cache is None:
        sdamgia = SdamGIA()
        catalog = sdamgia.get_catalog('math')
    else:
        catalog = catalog_cache
    list_of_types_ege = {}
    for i in range(Count_of_types):
        list_of_types_ege[catalog[i]['topic_id']] = catalog[i]['topic_name']
    #print(list_of_types_ege)
    return list_of_types_ege

def all_types_of_ege(catalog_cache=None):
    if catalog_cache is None:
        sdamgia = SdamGIA()
        catalog = sdamgia.get_catalog('math')
    else:
        catalog = catalog_cache
    count_of_all_types = 0
    while catalog[count_of_all_types]['topic_id'].isdigit():
        #print(catalog[count_of_all_types])
        count_of_all_types += 1
    return count_of_all_types




@dp.message_handler()
async def echosend(message: types.Message):
    await bot.send_message(message.from_user.id, 'Похоже произошли небольшие технические шоколадки')

executor.start_polling(dp, skip_updates=True)
