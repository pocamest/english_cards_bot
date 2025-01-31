import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from database import DataBase, add_default_words
from config_data import load_config, Config
from handlers import router
from middlewares import DataBaseMiddleware
from keyboards import set_main_menu
from services import DEFAULT_WORDS

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='[{asctime}] #{levelname:8} {filename}:'
        '{lineno} - {name} - {message}',
        style='{'
    )

    logger.info('Старт бота')

    config: Config = load_config()

    db = DataBase(url=config.db.url)

    storage = MemoryStorage()

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    session_factory = db.session_factory
    dp.update.middleware(DataBaseMiddleware(session_factory))
    dp.include_router(router)

    await db.create_db()
    async with session_factory() as session:
        await add_default_words(session, DEFAULT_WORDS)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
