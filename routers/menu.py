from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import get_menu_keyboard
from routers.reference import command_reference
from states import MenuStates, get_from_cache, put_to_cache
from templates import *

router = Router()


@router.message(Command(COMMAND_MENU))
async def command_menu(message: Message, state: FSMContext):
    greenhouse = await get_from_cache(message, state)

    sensor_lines = [
        MESSAGE_SENSOR.format(sensor.id, EMOJIS_SENSORS.get(sensor.type), sensor.reading, sensor.reference)
        for sensor in greenhouse.sensors
    ]
    controller_lines = [
        MESSAGE_CONTROLLER.format(
            controller.id, EMOJIS_SENSORS.get(controller.type), EMOJIS_STATUSES.get(controller.status)
        )
        for controller in greenhouse.controllers
    ]

    await state.set_state(MenuStates.IN_MAIN_MENU)
    await message.answer(
        MESSAGE_GREENHOUSE.format(greenhouse.device_id, "\n".join(sensor_lines), "\n".join(controller_lines)),
        reply_markup=get_menu_keyboard()
    )


@router.message(F.text == BUTTON_REFRESH)
async def button_refresh(message: Message, state: FSMContext):
    await put_to_cache(message.from_user.id, None)
    return await command_menu(message, state)


@router.message(F.text == BUTTON_BACK, MenuStates.PENDING_REFERENCE)
async def back_to_sensor(message: Message, state: FSMContext):
    await command_reference(message, state)


@router.message(F.text == BUTTON_BACK)
async def back_to_menu(message: Message, state: FSMContext):
    await button_refresh(message, state)
