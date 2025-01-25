from aiogram import Router
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message

from lexicon import LEXICON

from database import add_user, get_all_words
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import create_beginning_keyboard

from aiogram.fsm.state import default_state
from states import Training

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
    except Exception as e:
        logger.exception(f"Ошибка при обработке команды /start: {e}")



@router.message(Command(commands=['help']))
async def process_help(message: Message, session: AsyncSession):
    await message.answer(text=LEXICON['/help'])


@router.message(Command(commands=['beginning']), StateFilter(default_state))
async def process_beginning_without_training(
    message: Message, session: AsyncSession
):
    words = await get_all_words(session, message.from_user.id)
    await message.answer(
        text=LEXICON['/beginning_without_training'].format(len(words)),
        reply_markup=create_beginning_keyboard(
            'begin_training', 'cancel_training'
        )
    )


@router.message(
    Command(commands=['beginning']), StateFilter(Training.exists_training)
)
async def process_beginning_with_training(message: Message):
    await message.answer(
        text=LEXICON['/beginning_with_training'],
        reply_markup=create_beginning_keyboard(
            'continue_training', 'begin_new_training'
        )
    )
