from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from lexicon import LEXICON

from database import orm_add_user
from sqlalchemy.ext.asyncio import AsyncSession

import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def process_command_start(message: Message, session: AsyncSession):
    if message.from_user:
        await orm_add_user(
            session,
            user_name=message.from_user.first_name,
            tg_id=message.from_user.id
        )
        await message.answer(text=LEXICON['/start'])
    else:
        logger.warning('Ошибка: невозможно определить отправителя сообщения')
