from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import os

payment_token = "1744374395:TEST:4968087c11d2fa0ca11e"
Loop = asyncio.get_event_loop()

bot = Bot(token="5060681104:AAE4z8TcNxo0v-aSulDY1XqY_SzzvMaytSs", parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, storage=MemoryStorage(), loop=Loop)