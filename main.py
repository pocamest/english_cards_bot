import asyncio
import logging

from aiogram import Bot, Dispatcher
from database import DataBase
from config_data import load_config, Config
from handlers import router
from middlewares import DataBaseMiddleware
from aiogram.fsm.storage.memory import MemoryStorage

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

    router.message.middleware(DataBaseMiddleware(db.session_factory))
    dp.include_router(router)

    await db.create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
