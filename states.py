from aiogram.dispatcher.filters.state import StatesGroup, State

class States (StatesGroup):
    db_add = State()
    db_edit = State()