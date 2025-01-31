from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from lexicon import LEXICON

from database import add_user

from sqlalchemy.ext.asyncio import AsyncSession

import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def process_start(message: Message, session: AsyncSession):
    try:
        await add_user(
            session,
            user_name=message.from_user.first_name,
            tg_id=message.from_user.id
        )
        await message.answer(text=LEXICON['/start'])
    except Exception:
        logger.exception('Ошибка при обработке команды /start')


@router.message(Command(commands=['help']))
async def process_help(message: Message, session: AsyncSession):
    try:
        await message.answer(text=LEXICON['/help'])
    except Exception:
        logger.exception('Ошибка при обработки команды /help')