from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery

from lexicon import LEXICON

from database import add_card

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import create_generic_keyboard

from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from states import AddingCards

from filters import (
    IsCorrectWord, IsWordNotExists, IsCorrectTranslation
)

import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=['addcard']), StateFilter(default_state))
async def process_addcard(
    message: Message, state: FSMContext
):
    await state.set_state(AddingCards.adding_word)
    await message.answer(
        text=LEXICON['/addcard'],
        reply_markup=create_generic_keyboard('addcard_cancel')
    )


@router.callback_query(F.data == 'addcard_cancel')
async def process_addcard_cancel_press(
    callback: CallbackQuery, state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(text=LEXICON['addcard_cancel_text'])


@router.message(
    StateFilter(AddingCards.adding_word),
    IsCorrectWord(), IsWordNotExists()
)
async def process_correct_word(message: Message, state: FSMContext, word: str):
    await state.update_data(word=word)
    await state.set_state(AddingCards.adding_translation)
    await message.answer(
        text=LEXICON['correct_word'],
        reply_markup=create_generic_keyboard('addcard_cancel')
    )


@router.message(
    StateFilter(AddingCards.adding_word), IsCorrectWord(), ~IsWordNotExists()
)
async def process_word_exists(message: Message):
    await message.answer(
        text=LEXICON['word_exists'],
        reply_markup=create_generic_keyboard('addcard_cancel')
    )



@router.message(StateFilter(AddingCards.adding_word))
async def process_incorrect_word(message: Message):
    await message.answer(
        text=LEXICON['incorrect_word'],
        reply_markup=create_generic_keyboard('addcard_cancel')
    )


@router.message(
    StateFilter(AddingCards.adding_translation), IsCorrectTranslation()
)
async def process_correct_translation(
    message: Message, session: AsyncSession,
    state: FSMContext, translation: str
):
    data = await state.get_data()
    word = data['word']
    tg_id = message.from_user.id
    await add_card(session, tg_id, word, translation)
    await state.clear()
    await message.answer(
        text=LEXICON['correct_translation'].format(word, translation)
        )


@router.message(StateFilter(AddingCards.adding_translation))
async def process_incorrect_translation(message: Message):
    await message.answer(
        text=LEXICON['incorrect_translation'],
        reply_markup=create_generic_keyboard('addcard_cancel')
    )
