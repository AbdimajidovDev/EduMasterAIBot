from aiogram.fsm.state import State, StatesGroup

class SignUpState(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    email = State()
    password = State()
    confirm_password = State()
    code_verify = State()
    submit = State()


class LoginState(StatesGroup):
    email = State()
    password = State()


class CourseState(StatesGroup):
    selecting = State()