import asyncio
import logging

from aiogram import Bot, Dispatcher
from database import DataBase, add_default_words
from config_data import load_config, Config
from handlers import router
from middlewares import DataBaseMiddleware
from aiogram.fsm.storage.memory import MemoryStorage

logger = logging.getLogger(__name__)

DEFAULT_WORDS = [
    {"word": "белый", "translation": "white"},
    {"word": "чёрный", "translation": "black"},
    {"word": "красный", "translation": "red"},
    {"word": "синий", "translation": "blue"},
    {"word": "зелёный", "translation": "green"},
    {"word": "жёлтый", "translation": "yellow"},
    {"word": "оранжевый", "translation": "orange"},
    {"word": "фиолетовый", "translation": "purple"},
    {"word": "розовый", "translation": "pink"},
    {"word": "серый", "translation": "gray"}]


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

    session_factory = db.session_factory
    dp.update.middleware(DataBaseMiddleware(session_factory))
    dp.include_router(router)

    await db.create_db()
    if False:
        async with session_factory() as session:
            await add_default_words(session, DEFAULT_WORDS)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
