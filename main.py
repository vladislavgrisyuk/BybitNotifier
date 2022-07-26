import asyncio
import datetime
from pydoc import text
from tarfile import DEFAULT_FORMAT
from time import sleep
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message_entity import MessageEntity
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from order import order
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
import bybitApi

from trader import trader


load_dotenv()

storage = MemoryStorage()

token = os.getenv('TOKEN')
# api_key = os.getenv('API_KEY')
# api_secret = os.getenv('API_SECRET')

bot = Bot(token)
dp = Dispatcher(bot, storage=storage)
listOrders = []
URL = 'https://api2.bybit.com/fapi/beehive/public/v1/common/order/list-detail?timeStamp=1658218420604&leaderMark='
listTraders = [
    trader('faSUr%2Fa2JG%2FPv%2BvHa7Yoew%3D%3D', 'Moonpulse'),
    trader('vkbt1akj%2F7S0Xe3MB3bTgQ%3D%3D', 'Китаец топ-5'),
    trader('bTTxdRatXQ6XkYDX8mHgyw%3D%3D', 'Топ - 1 вернулся'),
    trader('lnOkBfOK6yeMGFaxdw4iFA%3D%3D', 'Китаец верняк'),
]

DEFAULT_QTY = os.getenv('DEFAULT_QTY')


@dp.message_handler(commands=['start', 'menu'])
async def begin(message: types.Message, state: FSMContext):
    first = True
    while(True):
        lm1 = 'faSUr%2Fa2JG%2FPv%2BvHa7Yoew%3D%3D'
        lm2 = 'vkbt1akj%2F7S0Xe3MB3bTgQ%3D%3D'
        lm3 = 'MPw0JFxXfu926mGwDpqPyA%3D%3D'
        lm4 = 'lnOkBfOK6yeMGFaxdw4iFA%3D%3D'

        # r = requests.get(URL + lm1)

        # data = json.loads(r.text)

        # await check_new_orders(data, first, message.chat.id, 'Moonpulse moi')
        # await check_if_close_orders(data, first, message.chat.id, 'MAIN Kitaec <3')

        # r = requests.get(URL + lm2)
        # data = json.loads(r.text)

        # await check_new_orders(data, first, message.chat.id, 'kitaec top-5')
        # await check_if_close_orders(data, first, message.chat.id, 'MAIN Kitaec <3')
        # r = requests.get(URL + lm3)
        # data = json.loads(r.text)

        # await check_new_orders(data, first, message.chat.id, 'CEO JEFFBZS TOP-1')
        # await check_if_close_orders(data, first, message.chat.id, 'MAIN Kitaec <3')

        r = requests.get(URL + lm4, headers={
            'User-Agent': 'vladislav'
        })
        data = json.loads(r.text)

        await check_new_orders(data, first, message.chat.id, 'Китаец верняк')
        await check_if_close_orders(data, first, message.chat.id, 'Китаец верняк')

        first = False


async def check_new_orders(data, first, chat_id, name=''):
    ll = await parseOrders(data)
    # if (first):
    #     ll.append(order('BTCUSDT', 'Sell', '3', '1232123', '5'))
    print(ll.__len__())
    for i in ll:
        if(not any(j.createdAt == i.createdAt for j in listOrders) or first):

            # if(first):
            #     i.is_created = False
            # else:
            f = float(i.entryPrice)

            v = 100 / float(f)

            nqty = float("{:.4f}".format(v))
            i.qty = nqty
            try:
                i.order_id = bybitApi.place_order(i.symbol, i.side, nqty)[
                    'result']['order_id']
                size = len(i.createdAt)
                await bot.send_message(chat_id,
                                       '✅✅✅\n' + name + '\n' + 'Монета: ' + i.symbol + '\n' + 'Вид: ' + i.side + '\n' + 'Курс входа: ' + i.entryPrice + '$' +
                                       '\n' + 'Время входа: ' + str(datetime.fromtimestamp(int(i.createdAt[:size - 3]))) + '\n' + 'Маржа: ' + i.leverage)

            except Exception as e:
                print(e)
            listOrders.append(i)


async def check_if_close_orders(data, first, chat_id, name=''):
    ll = await parseOrders(data)

    for i in listOrders:
        if(not any(j.createdAt == i.createdAt for j in ll)):
            listOrders.remove(i)
            size = len(i.createdAt)

            lside = 'Sell'
            if(i.side == 'Sell'):
                lside = 'Buy'

            if(i.is_created):
                try:
                    bybitApi.close_order(i.symbol, lside, i.qty)
                    await bot.send_message(chat_id,
                                           '㊗️㊗️㊗️\n' + name + '\n' + 'Монета: ' + i.symbol + '\n' + 'Вид: ' + i.side + '\n' + 'Курс входа: ' + i.entryPrice + '$' +
                                           '\n' + 'Время входа: ' + str(datetime.fromtimestamp(int(i.createdAt[:size - 3]))) + '\n' + 'Маржа: ' + i.leverage)

                except Exception as e:
                    print(e)


async def parseOrders(data):
    localList = []
    for i in data['result']['data']:
        localList.append(
            order(i['symbol'], i['side'], i['entryPrice'],
                  i['createdAtE3'], i['leverageE2'])
        )
    return localList


async def on_startup(dispatcher):
    commands = [
        {
            "command": "/start",
            "description": "Start the bot"
        },
    ]
    await bot.set_my_commands(commands)


executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
