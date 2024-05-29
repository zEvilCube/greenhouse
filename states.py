from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database.crud import read_auth
from server import get_greenhouse
from server.models import Greenhouse


class AuthStates(StatesGroup):
    PENDING_AUTH = State()


class MenuStates(StatesGroup):
    IN_MAIN_MENU = State()
    CHOOSING_SENSOR = State()
    PENDING_REFERENCE = State()


# Чтоб не обращаться к серверу каждый раз, когда нужны данные о теплице
async def put_to_cache(user_id: int, greenhouse: Greenhouse | None):
    cached_greenhouses.update({user_id: greenhouse})


async def get_from_cache(message: Message, state: FSMContext) -> Greenhouse:
    greenhouse = cached_greenhouses.get(message.from_user.id)
    if greenhouse is not None:
        return greenhouse

    greenhouse = get_greenhouse(read_auth(message.from_user.id).api_key)
    if greenhouse is not None:
        await put_to_cache(message.from_user.id, greenhouse)
        return greenhouse

    from routers import command_auth
    return await command_auth(message, state)


# Чтоб запомнить, эталон какого датчика меняет юзер
async def choose_sensor(user_id: int, sensor_id: int):
    chosen_sensors.update({user_id: sensor_id})


async def get_chosen_sensor(user_id: int) -> int:
    return chosen_sensors.get(user_id, -1)


cached_greenhouses = {}
chosen_sensors = {}
