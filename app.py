# -*- coding: utf-8 -*-
from aiogram import executor
from main import dp
def start():
    executor.start_polling(dispatcher=dp)

start()