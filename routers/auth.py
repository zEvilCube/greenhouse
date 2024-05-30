from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.crud import update_auth
from server import get_greenhouse
from states import AuthStates
from templates import *

router = Router()


@router.message(Command(COMMAND_AUTH))
@router.message(F.text == BUTTON_AUTH)
async def command_auth(message: Message, state: FSMContext):
    await state.set_state(AuthStates.PENDING_AUTH)
    await message.answer(MESSAGE_AUTH_PENDING)


@router.message(AuthStates.PENDING_AUTH)
async def pending_auth(message: Message, state: FSMContext):
    from routers.menu import button_refresh
    if get_greenhouse(message.text) is None:
        return await message.answer(MESSAGE_AUTH_INVALID)
    update_auth(message.from_user.id, message.text)
    return await button_refresh(message, state)
