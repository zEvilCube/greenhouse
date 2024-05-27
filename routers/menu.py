from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import MenuStates
from templates import *

router = Router()


@router.message(Command(COMMAND_MENU))
async def command_menu(message: Message, state: FSMContext):
    await state.set_state(MenuStates.IN_MAIN_MENU)
    await message.answer(MESSAGE_MENU, reply_markup=None)
