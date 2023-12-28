from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

#стартовая клавиатура
user_kb = InlineKeyboardMarkup(inline_keyboard=
    [
        [
            InlineKeyboardButton(text="Расписание сегодня"
                                ,callback_data='schedule:today')
        ],
        [
            InlineKeyboardButton(text="Изменить БД", callback_data="db:edit")
        ],
        [
            InlineKeyboardButton(text="Добавить в БД", callback_data="db:add")
        ],
        [
            InlineKeyboardButton(text="Посмотреть БД", callback_data="db:check")
        ]
    ])

#
async def DB_choise(data:dict,mod:str):
    kb = InlineKeyboardMarkup(inline_keyboard=[],row_width=2)
    btns = []
    if mod =='add':
        for btn_name,db_name in data.items():
            btns.append(InlineKeyboardButton(text=btn_name,
                                             callback_data=f'db_add:{db_name}'
                                             )
                           )
    elif mod == 'edit':
        for btn_name, db_name in data.items():
            btns.append(InlineKeyboardButton(text=btn_name,
                                             callback_data=f'db_edit:{db_name}'
                                             )
                           )

    kb.add(*btns)
    kb.row(InlineKeyboardButton(text='В меню',callback_data='menu'))
    return kb

back_mn_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='В меню', callback_data='menu')
    ]
])

remove_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Скрыть', callback_data='remove_it')
    ]
])
async def cancel_kb(mode='',table=None,id=None):
    kb = InlineKeyboardMarkup(inline_keyboard=[])
    if mode == 'edit':
        kb.row(InlineKeyboardButton(text='Удалить',
                                    callback_data=f'db_rem:{table}_{id}'))
    kb.row(InlineKeyboardButton(text='Отмена',
                                callback_data=f'cancel:{mode}'))
    return kb


[]
async def db_edit_select(data:list):
    kb = InlineKeyboardMarkup(inline_keyboard=[],row_width=1)
    buttons = [
        InlineKeyboardButton(text=f"{'|'.join([str(name) for name in btn])}",
        callback_data=f'db_edit2:{btn[0]}') for btn in data
              ]
    kb.add(*buttons)
    kb.row(InlineKeyboardButton(text='Назад',callback_data='db:edit'))
    return kb