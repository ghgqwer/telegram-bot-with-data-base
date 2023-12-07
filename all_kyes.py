from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='')#your bot token
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
