import pyqiwi
from pyqiwip2p import QiwiP2P

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.misc.connection import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# DB
db = Database()


# Qiwi
p2p = QiwiP2P(auth_key = config.QIWI_P2P_TOKEN)
wallet = pyqiwi.Wallet(token = config.QIWI_TOKEN, number = config.QIWI_NUMBER)