from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from lexicon import LEXICON

from database import (
    get_all_words,
    delete_word,
)

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import create_cards_keyboard

from services import get_translation_optionals
from filters import IsPage, IsDeleteWord

import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=['cards']))
async def process_cards(message: Message, session: AsyncSession):
    word_translations = await get_all_words(session, message.from_user.id)
    await message.answer(
        text=LEXICON['/cards'].format(len(word_translations)),
        reply_markup=create_cards_keyboard(word_translations)
    )


@router.callback_query(IsPage())
async def process_pagination_press(
    callback: CallbackQuery, session: AsyncSession, page: int
):
    word_translations = await get_all_words(session, callback.from_user.id)
    await callback.message.edit_reply_markup(
        reply_markup=create_cards_keyboard(word_translations, page)
    )


@router.callback_query(IsDeleteWord())
async def process_delete_press(
    callback: CallbackQuery, session: AsyncSession, word: str
):
    try:
        tg_id = callback.from_user.id
        await delete_word(session, tg_id, word)
        await callback.message.edit_text(
            text=LEXICON['delete_word'].format(word)
        )
    except Exception:
        logger.exception(f'Ошибка при удалении слова {word}')