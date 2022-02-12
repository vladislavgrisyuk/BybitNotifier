import datetime
from pydoc import text
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message_entity import MessageEntity
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from talent import talentS
import pdfhelper
import helper
from replacements import get_replacement_with_time, get_replacements
from random import randint
import os
from dotenv import load_dotenv
from timeGenerator import generate_with_random_time
from menu_keyboard import kb

load_dotenv()

storage = MemoryStorage()

token = os.getenv('TOKEN')


bot = Bot(token)
dp = Dispatcher(bot, storage=storage)


class UserState(StatesGroup):
    base = State()
    choose = State()
    Chosen = State()


@dp.message_handler(commands=['start', 'menu'])
async def begin(message: types.Message, state: FSMContext):
    await message.answer('Menu', reply_markup=kb)


@dp.message_handler(commands=['vlad'])
@dp.message_handler(text=['Влад тест'])
async def begin(message: types.Message, state: FSMContext):
    pdfhelper.go('Resources/v.pdf', get_replacements())
    await bot.send_document(message.chat.id, document=open('Resources/v.result.pdf', 'rb'))
    os.remove('Resources/v.result.pdf')


@dp.message_handler(commands=['nastya'])
@dp.message_handler(text=['Настя тест'])
async def begin(message: types.Message):
    r = get_replacements()
    pdfhelper.go('Resources/n.pdf', r)
    await bot.send_document(message.chat.id, document=open('Resources/n.result.pdf', 'rb'))
    os.remove('Resources/n.result.pdf')


@dp.message_handler(commands=['all'])
@dp.message_handler(text=['Оба теста'])
async def begin(message: types.Message):
    r_small = randint(2, 5)
    time_gen = generate_with_random_time(9, 13)
    r_time_hours = time_gen.hour
    r_time_minutes = time_gen.minute

    time = str(r_time_hours).zfill(2) + ':' + str(r_time_minutes).zfill(2)

    time_gen_delta = time_gen + datetime.timedelta(minutes=15+r_small)
    time_minutes_delta = r_time_minutes + 15
    time_delta = str(r_time_hours).zfill(2) + ':' + \
        str(time_minutes_delta).zfill(2)

    r = get_replacements(r_time_hours, r_time_minutes)
    r2 = get_replacement_with_time(time_gen, time_gen_delta)
    pdfhelper.go('Resources/n.pdf', r2)
    await bot.send_document(message.chat.id, document=open('Resources/n.result.pdf', 'rb'))

    r = get_replacements(r_time_hours, r_time_minutes + r_small)
    r2 = get_replacement_with_time(time_gen + datetime.timedelta(
        minutes=r_small), time_gen_delta + datetime.timedelta(minutes=r_small))
    pdfhelper.go('Resources/v.pdf', r2)
    await bot.send_document(message.chat.id, document=open('Resources/v.result.pdf', 'rb'))

    os.remove('Resources/n.result.pdf')
    os.remove('Resources/v.result.pdf')


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
        },
        {
            "command": "/menu",
            "description": "Menu buttons"
        }
    ]
    await bot.set_my_commands(commands)


executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
