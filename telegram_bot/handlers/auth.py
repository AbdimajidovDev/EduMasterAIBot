from aiogram.types import Message
from aiogram import F, Router
from telegram_bot.loader import dp
from telegram_bot.states.auth_states import LoginState
from telegram_bot.utils.api import api_request
from telegram_bot.utils.storage import save_token

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()


@dp.message(Command('start'))
async def start_answer(message: Message, state: FSMContext):
    await message.answer(f"Assalomu alaykum {message.from_user.full_name} 👋\n Tizimga kirish (/login or /signup)")


@dp.message(Command('help'))
async def help_answer(message: Message):
    await message.answer("""<b>Bot buyruqlari</b>
    /start - Botni ishga tushirish
    /help - Yordam olish
    /signup - Signup
    /login - Tizimga kirish
    /courses - Mavjud kurslar ko'rish

    📞 Call center: +998955710660
    🧑🏻‍💼 Admin: @Abdimajidov_oo1""")

@router.message(F.text == '/login')
async def login(message: Message, state: FSMContext):
    await message.answer("📧 Emailingizni kiriting:")
    await state.set_state(LoginState.email)


@dp.message(LoginState.email)
async def get_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Parolingizni kiriting:")
    await state.set_state(LoginState.password)


@dp.message(LoginState.password)
async def get_password(message: Message, state: FSMContext):
    user_data = await state.get_data()
    email = user_data['email']
    password = message.text

    response = await api_request("POST", "/telegram-bot/auth/login/", data={"email": email, "password": password})

    if 'access' in response:
        await save_token(message.from_user.id, response['access'])
        await message.answer("✅ Tizimga muvofaqiyatli kirildi!")
        await state.clear()
    else:
        await message.answer(f"❌ Xatolik: {response}! Qayta urinib ko'ring.")
        # await state.clear()

# @dp.message(Command('stop'))
# async def stop_answer(message: Message, state: FSMContext):
#     await message.answer('saloooom')
#     print(state)
#     if state:
#         print(state)
#         await state.clear()
#     else:
#         print(state.get_data())

    # await message.answer()