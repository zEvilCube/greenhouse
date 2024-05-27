from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

common_router = Router()


@common_router.message(Command("start"))
async def command_start(message: Message, state: FSMContext):
    await message.answer("NOTHING HERE YET")


@common_router.message(Command("help"))
async def command_help(message: Message, state: FSMContext):
    await message.answer("NOTHING HERE YET")


@common_router.message()
async def test(message: Message, state: FSMContext):
    await message.answer("Hello, World!")
