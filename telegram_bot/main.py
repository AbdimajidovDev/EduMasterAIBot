import logging
from aiogram import Bot
from asyncio import run
from telegram_bot.config import ADMIN_ID
from telegram_bot.loader import dp, bot
from telegram_bot.handlers import auth, course, user

logging.basicConfig(level=logging.INFO)




async def startup_answer(bot: Bot):
    await bot.send_message(ADMIN_ID, "Bot ishga tushdi!")

async def shutdown_answer(bot: Bot):
    await bot.send_message(ADMIN_ID, "Bot ishdan to'xtadi!")


async def main():
    # bot = Bot(token=BOT_TOKEN)

    dp.startup.register(startup_answer)
    dp.shutdown.register(shutdown_answer)

    dp.include_router(auth.router)
    dp.include_router(course.router)
    dp.include_router(user.router)

    await dp.start_polling(bot)

run(main())
