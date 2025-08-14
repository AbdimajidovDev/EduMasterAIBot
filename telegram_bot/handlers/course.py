from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message

from telegram_bot.utils.api import api_request
from telegram_bot.utils.storage import get_token

router = Router()

@router.message(Command("courses"))
async def list_courses(message: Message):
    token = await get_token(message.from_user.id)
    print('token:', token)
    if token is None:
        token = await message.answer("❌ Avval /login orqali tizimga kiring.")
        return

    courses = await api_request("GET", "/course/", token=token)
    print('bool', "error" in courses)
    if "error" in courses:
        print('courses', courses)
        await message.answer(f"❌ Xatolik: {courses['message']}")
        return

    text = "📚 Kurslaringiz: \n\n" + '\n'.join(f"* {c['title']}" for c in courses)
    print(text)
    await message.answer(text)
