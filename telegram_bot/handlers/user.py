from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from telegram_bot.loader import dp
from telegram_bot.states.auth_states import SignUpState
from telegram_bot.utils.api import api_request
from telegram_bot.utils.storage import save_token

router = Router()


@router.message(F.text == '/signup')
async def signup(message: Message, state: FSMContext):
    await message.answer('Ismingizni kiriting:')
    await state.set_state(SignUpState.first_name)


@dp.message(SignUpState.first_name)
async def signup_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer('Familiyangizni kiriting')
    await state.set_state(SignUpState.last_name)

@dp.message(SignUpState.last_name)
async def signup_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Telefon raqamingizni yuboring.")
    await state.set_state(SignUpState.phone_number)


@dp.message(SignUpState.phone_number)
async def signup_phone_number(message: Message, state:FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Emailingizni kiriting.")
    await state.set_state(SignUpState.email)

@dp.message(SignUpState.email)
async def signup_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Parolingizni kiriting.")
    await state.set_state(SignUpState.password)

@dp.message(SignUpState.password)
async def signup_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer('Tasdiqlash parolingizni kiriting.')
    await state.set_state(SignUpState.confirm_password)

@dp.message(SignUpState.confirm_password)
async def signup_confirm_password(message: Message, state: FSMContext):
    await state.update_data(confirm_password=message.text)
    user_data = await state.get_data()
    email = user_data['email']
    await message.answer(f'{email} emailiga yuborilgan tasdiqlash kodni kiriting.')
    await state.set_state(SignUpState.code_verify)


@dp.message(SignUpState.code_verify)
async def signup_code_verify(message: Message, state: FSMContext):
    await state.update_data(code_verify=message.text)
    await message.answer("Malumotlaringiz qabul qilindi.")

    user_data = await state.get_data()
    first_name = user_data['first_name']
    last_name = user_data['last_name']
    phone_number = user_data['phone_number']
    email = user_data['email']
    password = user_data['password']
    confirm_password = user_data['confirm_password']

    response = await api_request("POST", "/telegram-bot/auth/signup/",
                                 data={
                                     "first_name": first_name,
                                     "last_name": last_name,
                                     "phone_number": phone_number,
                                     "email": email,
                                     "password": password,
                                     "confirm_password": confirm_password,
                                 })
    print('response:', response)

    if response:
        await message.answer("✅ Ro'yxatdan muvofaqiyatli o'tdingiz!")
        await state.clear()
    else:
        await message.answer(f"❌ Xatolik: {response}! Qayta urinib ko'ring (/signup).")
    await state.clear()

    await message.answer("Ro'yxatdan o'tish (yes|no)")
    await state.set_state(SignUpState.submit)


@dp.message(SignUpState.submit)
async def signup_submit(message: Message, state: FSMContext):
    if message.text.lower() == 'yes':
        pass
    elif message.text.lower() == 'no':
        await message.answer("Ro'yxatdan o'tish bekor qilindi!")
        await state.clear()
    else:
        await message.answer("Noto'g'ri so'rov")




