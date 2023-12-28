import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import inl_keyboards as in_kb
from states import States
from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from config import bot_token
from db_scr import *
from datetime import datetime


bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)


# Функция СТАРТ/МЕНЮ И т.д

@dp.callback_query_handler(text='menu', state='*')
async def call_start(call: CallbackQuery):
    cur_state = dp.current_state(user=call.from_user.id)
    await cur_state.reset_state()
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text='Выберите вариант',
                                reply_markup=in_kb.user_kb)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message):
    cur_state = dp.current_state(user=message.from_user.id)
    await cur_state.reset_state()
    await message.answer('Выберите вариант', reply_markup=in_kb.user_kb)

# start ends
# commands Посмотреть данные

@dp.message_handler(commands=['subjects'])
async def show_subj(message: types.Message):
    await message.delete()
    subj = await get_table_data('subjects')
    col_names = await get_collumn_names('subjects')
    names = [name[1] for name in col_names]
    subj.insert(0, names)
    text = (f'Таблица: {message.text.replace("/", "")}\n' +
            '\n'.join([f'{line[0]}|{line[1]}' for line in subj]))
    await message.answer(text=text, reply_markup=in_kb.remove_kb)


@dp.message_handler(commands=['time'])
async def show_subj(message: types.Message):
    await message.delete()
    subj = await get_table_data('time')
    col_names = await get_collumn_names('time')
    names = [name[1] for name in col_names]
    subj.insert(0, names)
    text = (f'Таблица: {message.text.replace("/", "")}\n' +
            '\n'.join([f'{line[0]}|{line[1]}' for line in subj]))
    await message.answer(text=text, reply_markup=in_kb.remove_kb)


@dp.message_handler(commands=['cabinets'])
async def show_subj(message: types.Message):
    await message.delete()
    subj = await get_table_data('cabinets')
    col_names = await get_collumn_names('cabinets')
    names = [name[1] for name in col_names]
    subj.insert(0, names)
    text = (f'Таблица: {message.text.replace("/", "")}\n' +
            '\n'.join([f'{line[0]}|{line[1]}' for line in subj]))
    await message.answer(text=text, reply_markup=in_kb.remove_kb)


@dp.message_handler(commands=['teachers'])
async def show_subj(message: types.Message):
    await message.delete()
    subj = await get_table_data('teachers')
    col_names = await get_collumn_names('teachers')
    names = [name[1] for name in col_names]
    subj.insert(0, names)
    text = (f'Таблица: {message.text.replace("/", "")}\n' +
            '\n'.join([f'{line[0]}|{line[1]}' for line in subj]))
    await message.answer(text=text, reply_markup=in_kb.remove_kb)

# commands ends
# Функции call(db) стартовые

@dp.callback_query_handler(text_contains='db:', state='*')
async def db(call: CallbackQuery):
    req = call.data[3:]
    if req == 'add':
        text = 'Выберите что хотите добавить.'
        kb = await in_kb.DB_choise(config.tables, mod='add')
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=kb)
    elif req == 'edit':
        text = 'Выберите что хотите изменить.'
        kb = await in_kb.DB_choise(config.tables, mod='edit')
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=kb)
    elif req == 'check':
        kb = in_kb.back_mn_kb
        text = (f'\nПосмотрите данные'
                f'\n/teachers -- Преподаватели'
                f'\n/cabinets -- Кабинеты'
                f'\n/subjects -- Предметы'
                f'\n/time -- Учебное время')
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=kb)


@dp.callback_query_handler(text_contains='db_add:', state='*')
async def db_add(call: CallbackQuery, state: FSMContext):
    table = call.data[7:]
    async with state.proxy() as data:
        data['table'] = table
    cur_state = dp.current_state(user=call.from_user.id)
    await cur_state.set_state(States.db_add)
    columns_names = await get_collumn_names(table)
    i = 0
    for name in columns_names:
        if name[5] == 1:
            columns_names.remove(name)
        else:
            i += 1
        if name[1] == 'date':
            columns_names[i] = list(columns_names[i])
            columns_names[i][2] = str(
                datetime.now().date().strftime('%d.%m.%Y'))
    kb = await in_kb.cancel_kb('add')
    if len(columns_names) > 1:
        text = (f'Введите новые значения через |'
                f'\nФормат: {"|".join([name[1] for name in columns_names])}'
                f'\nПример: <code>'
                f'{"|".join([f"{name[2]}" for name in columns_names])}</code>'
                f'\n\nПосмотрите данные'
                f'\n/teachers -- Преподаватели'
                f'\n/cabinets -- Кабинеты'
                f'\n/subjects -- Предметы'
                f'\n/time -- Учебное время')
    else:
        if table == "teachers":
            example = 'Иванов Иван Иванович'
        else:
            example = "|".join([name[2] for name in columns_names])
        text = (f'Введите значение для добавления'
                f'\n{table}'
                f'\nФормат: <code>{example}</code>')
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=kb)


@dp.callback_query_handler(text_contains='db_edit:', state='*')
async def db_edit(call: CallbackQuery, state: FSMContext):
    table = call.data[8:]
    async with state.proxy() as data:
        data['table'] = table
    data = await get_table_data(table)
    columns_names = await get_collumn_names(table)
    kb = await in_kb.db_edit_select(data)
    text = (f'Выберите обьект для редактирования'
            f'\n<b>{table}</b>'
            f'\n{"|".join([name[1] for name in columns_names])}')
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=kb)


@dp.callback_query_handler(text_contains='db_edit2:', state='*')
async def db_edit2(call: CallbackQuery, state: FSMContext):
    id = call.data[9:]
    async with state.proxy() as data:
        data['id'] = id
        table = data['table']
    cur_state = dp.current_state(user=call.from_user.id)
    await cur_state.set_state(States.db_edit)
    columns_names = await get_collumn_names(table)
    i = 0
    for name in columns_names:
        if name[5] == 1:
            columns_names.remove(name)
        else:
            i += 1
        if name[1] == 'date':
            columns_names[i] = list(columns_names[i])
            columns_names[i][2] = str(
                datetime.now().date().strftime('%d.%m.%Y'))
    kb = await in_kb.cancel_kb('edit', table, id)
    if len(columns_names) > 1:
        text = (
            f'Введите новые значения через |'
            f'\n{table}  (id:{id})'
            f'\nФормат: <code>'
            f'{"|".join([f"{name[1]}={name[2]}" for name in columns_names])}</code>'
            f'\n\nПосмотрите данные'
            f'\n/teachers -- Преподаватели'
            f'\n/cabinets -- Кабинеты'
            f'\n/subjects -- Предметы'
            f'\n/time -- Учебное время'
        )
    else:
        if table == "teachers":
            example = 'id=INT|name=Иванов Иван Иванович'
        else:
            example = "|".join(
                [f"{name[1]}={name[2]}" for name in columns_names])
        text = (f'Введите новое значение'
                f'\n{table}  (id:{id})'
                f'\nФормат: {"|".join([name[1] for name in columns_names])}'
                f'\nПример: <code>{example}</code>')
    await bot.edit_message_text(chat_id=call.from_user.id,
                                message_id=call.message.message_id,
                                text=text,
                                reply_markup=kb)


@dp.callback_query_handler(text_contains='db_rem:', state='*')
async def db_rem(call: CallbackQuery):
    cmd = call.data[7:].split('_')
    if await remove_from_db(cmd[0], cmd[1]):
        await call.answer('Успешное удаление', show_alert=True)
        cur_state = dp.current_state(user=call.from_user.id)
        await cur_state.reset_state()
        text = 'Выберите что хотите изменить.'
        kb = await in_kb.DB_choise(config.tables, mod='edit')
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=kb)
    else:
        await call.answer('Неудачное удаление'
                          '\nСвяжитесь с администратором.',
                          show_alert=True)


@dp.callback_query_handler(text_contains='cancel:', state='*')
async def cancel_handler(call: CallbackQuery):
    req = call.data[7:]
    if req == 'add':
        cur_state = dp.current_state(user=call.from_user.id)
        await cur_state.reset_state()
        text = 'Выберите что хотите добавить.'
        kb = await in_kb.DB_choise(config.tables, mod='add')
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=kb)
    elif req == 'edit':
        cur_state = dp.current_state(user=call.from_user.id)
        await cur_state.reset_state()
        text = 'Выберите что хотите изменить.'
        kb = await in_kb.DB_choise(config.tables, mod='edit')
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=kb)


# Функции message_db (add,edit)

@dp.message_handler(state=States.db_add)
async def add_db(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        table = data['table']
    columns_names = await get_collumn_names(table)
    full_col_names = list(columns_names)
    kb = await in_kb.cancel_kb('add')
    i = 0
    for name in columns_names:
        if name[5]:
            columns_names.remove(name)
        else:
            i += 1
        if name[1] == 'date':
            columns_names[i] = list(columns_names[i])
            columns_names[i][2] = str(
                datetime.now().date().strftime('%d.%m.%Y'))
    if len(msg.split('|')) == len(columns_names):
        msg = msg.split('|')
        status = True
        for i in range(len(columns_names)):
            if columns_names[i][2] == 'INT' and not msg[i].isdigit():
                await message.answer(
                    text=f'Неверный формат {columns_names[i][1]}',
                    reply_markup=kb)
                status = False
                break
        if status:
            await insert_new_values(table, full_col_names, msg)
            await message.answer('Успешное добавление!')
            await start(message)
    else:
        await message.answer(text='Неверный формат',
                             reply_markup=kb)


@dp.message_handler(state=States.db_edit)
async def edit_db(message: types.Message, state: FSMContext):
    msg = message.text
    async with state.proxy() as data:
        table = data['table']
        id = data['id']
    columns_names = await get_collumn_names(table)
    kb = await in_kb.cancel_kb('add')
    i = 0
    for name in columns_names:
        if name[5]:
            columns_names.remove(name)
        else:
            i += 1
        if name[1] == 'date':
            columns_names[i] = list(columns_names[i])
            columns_names[i][2] = str(
                datetime.now().date().strftime('%d.%m.%Y'))
    if len(msg.split('|')) == len(columns_names):
        msg = msg.split('|')
        status = True
        cols = []
        vals = []
        for i in range(len(columns_names)):
            try:
                col, val = msg[i].split('=')
                cols.append(col)
                vals.append(val)
                if columns_names[i][2] == 'INT' and not val.isdigit():
                    await message.answer(
                        text=f'Неверный формат {columns_names[i][1]}',
                        reply_markup=kb
                    )
                    status = False
                    break
                if columns_names[i][1] != cols[i]:
                    await message.answer(
                        'Ошибка'
                        f'\nПараметра {cols[i]} не существует',
                        reply_markup=kb
                    )
                    status = False
                    break
            except ValueError:
                status = False
                await message.answer(
                    text=f'Неверный формат {columns_names[i][1]}',
                    reply_markup=kb)
                break
        if status:
            resp = await edit_values(table, cols, vals, id)
            if resp:
                await message.answer('Успешное изменение!')
                await start(message)
            else:
                await message.answer(
                    'Ошибка'
                    '\nВероятно вы пытаетесь установить занятый id'
                    '\nПовторите попытку.',
                    reply_markup=kb)
    else:
        await message.answer(text='Неверный формат',
                             reply_markup=kb)


# Вспомогательное (Удаление сообщения)
@dp.callback_query_handler(text='remove_it', state='*')
async def remove_msg(call: CallbackQuery):
    await bot.delete_message(chat_id=call.from_user.id,
                             message_id=call.message.message_id)


# Пользовательская часть - расписание
@dp.callback_query_handler(text_contains='schedule:', state='*')
async def schedule(call: CallbackQuery):
    day = call.data[9:]
    if day == 'today':
        cur_date = datetime.now().date().strftime("%d.%m.%Y")
        data = await get_shedule(str(cur_date))
        data.sort(key=lambda elem: elem[4])  # sort by time id
        from config import weekdays
        cur_dateday = weekdays[
            datetime.strptime(
                str(cur_date),
                "%d.%m.%Y"
            ).weekday()
        ]
        text = (f'Расписание на ({cur_dateday})'
                f'\n<b>{cur_date}</b>')
        cur_time = ''
        for line in data:
            time = await get_values(
                'time', ['value'], line[4]
            )
            time = time[0]
            teacher = await get_values(
                'teachers', ['name'], line[1]
            )
            teacher = teacher[0]
            cab_seats = await get_values(
                'cabinets', ['seats'], line[3]
            )
            cab_seats = cab_seats[0]
            subject = await get_values(
                'subjects', ['name'], line[2]
            )
            subject = subject[0]
            if cur_time != time:
                text += f"\n\n----------------\n\n{time}"
                cur_time = time
            text += (f'\n(Каб. <b>{line[3]}</b> | Мест {cab_seats}) {subject}'
                     f'\n<b>{teacher}</b>')
        await bot.edit_message_text(chat_id=call.from_user.id,
                                    message_id=call.message.message_id,
                                    text=text,
                                    reply_markup=in_kb.back_mn_kb)
