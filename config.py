from environs import Env
env = Env()

env.read_env('settings.env')
bot_token = env.str('bot_token')

tables = {'Преподаватели':'teachers',
          'Кабинеты':'cabinets',
          'Предметы':'subjects',
          'Учебное время':'time',
          'Расписание':'shedule'}

weekdays = {0:'Пн',1:'Вт',2:'Ср',3:'Чт',4:'Пт',5:'Сб',6:'Вс'}

