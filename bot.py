import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from database import models, engine
from routers import common_router, auth, menu, reference


async def main():
    models.Base.metadata.create_all(bind=engine)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    bot = Bot(config.bot_token.get_secret_value())
    dispatcher = Dispatcher(storage=MemoryStorage())
    dispatcher.include_routers(auth.router, menu.router, reference.router, common_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
