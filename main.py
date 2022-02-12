import datetime
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message_entity import MessageEntity
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from talent import talentS
import pdfhelper
import helper
from replacements import get_replacement_with_time, getReplacementsV
from random import randint
import os
from dotenv import load_dotenv
from timeGenerator import generate_with_random_time

load_dotenv()

storage = MemoryStorage()

token = os.getenv('TOKEN')


bot = Bot(token)
dp = Dispatcher(bot, storage=storage)


class TalentState(StatesGroup):
    base = State()
    choose = State()
    Chosen = State()


@dp.message_handler(commands=['vlad'])
async def begin(message: types.Message, state: FSMContext):
    pdfhelper.go('v.pdf', getReplacementsV())
    await bot.send_document(message.chat.id, document=open('v.result.pdf', 'rb'))



@dp.message_handler(commands=['nastya'])
async def begin(message: types.Message):
    r = getReplacementsV()
    pdfhelper.go('n.pdf', r)
    await bot.send_document(message.chat.id, document=open('n.result.pdf', 'rb'))
    
@dp.message_handler(commands=['all'])
async def begin(message: types.Message):
    rSmall = randint(2, 5)
    time_gen = generate_with_random_time(9, 13)
    rTimeHours = time_gen.hour
    rTimeMinutes = time_gen.minute
    
    time = str(rTimeHours).zfill(2) + ':' + str(rTimeMinutes).zfill(2)
    
    time_gen_delta = time_gen + datetime.timedelta(minutes=15+rSmall)
    timeMinutesPlus = rTimeMinutes + 15
    timePlus = str(rTimeHours).zfill(2) + ':' + str(timeMinutesPlus).zfill(2)
    
    r = getReplacementsV(rTimeHours, rTimeMinutes)
    r2 = get_replacement_with_time(time_gen, time_gen_delta)
    pdfhelper.go('n.pdf', r2)
    await bot.send_document(message.chat.id, document=open('n.result.pdf', 'rb'))
    
    r = getReplacementsV(rTimeHours, rTimeMinutes + rSmall)
    r2 = get_replacement_with_time(time_gen + datetime.timedelta(minutes=rSmall), time_gen_delta + datetime.timedelta(minutes=rSmall))
    pdfhelper.go('v.pdf', r2)
    await bot.send_document(message.chat.id, document=open('v.result.pdf', 'rb'))


async def on_startup(dispatcher):
    commands = [
        {
            "command": "/nastya",
            "description": "Certificate for nastya"
        },
        {
            "command": "/vlad",
            "description": "Certificate for vlad"
        },
        {
            "command": "/all",
            "description": "Both certificates"
        }
    ]
    await bot.set_my_commands(commands)


executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

# if __name__ == '__main__':
#     main()