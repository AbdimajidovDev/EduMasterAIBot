from aiogram import Bot, Dispatcher

from telegram_bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()