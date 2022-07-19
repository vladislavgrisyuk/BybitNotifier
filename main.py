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
import logging
import sys
import requests
import json
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt='%Y.%m.%d %H:%M:%S',
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

load_dotenv()

storage = MemoryStorage()

token = os.getenv('TOKEN')

bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
listOrders = []


class UserState(StatesGroup):
    base = State()
    choose = State()
    Chosen = State()


@dp.message_handler(commands=['start', 'menu'])
async def begin(message: types.Message, state: FSMContext):
    first = True
    while(True):
        lm1 = 'IT3R2gEhFD0qI%2FL7r3FS5g%3D%3D'
        lm2 = 'bTTxdRatXQ6XkYDX8mHgyw=='
        url = 'https://api2.bybit.com/fapi/beehive/public/v1/common/order/list-detail?timeStamp=1658218420604&leaderMark='

        r = requests.get(url + lm1)

        data = json.loads(r.text)

        await bot.send_message(message.chat.id, bbt_data(data, first))

        r = requests.get(url + lm2)

        data = json.loads(r.text)

        await bot.send_message(message.chat.id, bbt_data(data, first))
        first = False


def bbt_data(data, first):
    for i in data['result']['data']:
        if(not listOrders.__contains__(i['createdAtE3']) or first):
            listOrders.append(i['createdAtE3'])
            size = len(i['createdAtE3'])

            return 'Монета: ' + i['symbol'] + '\n' + 'Вид: ' + i['side'] + '\n' + 'Курс входа: ' + i['entryPrice'] + '$' + '\n' + 'Время входа: ' + str(datetime.fromtimestamp(int(i['createdAtE3'][:size - 3]))) + '\n' + 'Маржа: ' + i['leverageE2']


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
