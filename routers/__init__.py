from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from routers.auth import command_auth
from templates import *

common_router = Router()


@common_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    await message.answer(MESSAGE_GREETING.format(message.from_user.full_name))
    await command_auth(message, state)


@common_router.message(Command("help"))
async def command_help(message: Message, state: FSMContext):
    await message.answer(MESSAGE_HELP)
