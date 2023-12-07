from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='6331553602:AAEAILCnp7Kx1SPXaAlgrtt_s9hsa2BmgYk')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
