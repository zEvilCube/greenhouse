from aiogram.fsm.state import State, StatesGroup


class AuthStates(StatesGroup):
    PENDING_AUTH = State()


class MenuStates(StatesGroup):
    IN_MAIN_MENU = State()
