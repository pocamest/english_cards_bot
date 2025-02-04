from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery

from lexicon import LEXICON

from database import (get_all_words)

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import (
    create_generic_keyboard,
    create_training_keyboard
)

from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from states import Training

from services import get_translation_optionals

import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=['beginning']), StateFilter(default_state))
async def process_beginning_without_training(
    message: Message, session: AsyncSession
):
    try:
        word_translations = await get_all_words(session, message.from_user.id)
        await message.answer(
            text=LEXICON['/beginning_without_training'].format(
                len(word_translations)
            ),
            reply_markup=create_generic_keyboard(
                'begin_training', 'cancel_training'
            )
        )
    except Exception:
        logger.exception('Ошибка при обработке команды /beginning')


@router.callback_query(
    F.data.in_(['begin_training', 'begin_new_training'])
)
async def process_begin_training_press(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    try:
        await state.clear()
        await state.set_state(Training.exists_training)

        word_translations = await get_all_words(session, callback.from_user.id)
        word_iter = iter(word_translations)

        await state.update_data(
            word_translations=word_translations, word_iter=word_iter
        )

        current_word = next(word_iter)

        translation, optionals = get_translation_optionals(
            word_translations, current_word
        )
        await callback.message.edit_text(
            text=LEXICON['training_text'].format(current_word),
            reply_markup=create_training_keyboard(
                translation, optionals
            )
        )
    except Exception:
        logger.exception('Ошибка при обработке начала тренировки')


# Подумать над дублированием кода
@router.callback_query(
    F.data == 'right_answer', StateFilter(Training.exists_training)
)
async def process_right_answer_press(
    callback: CallbackQuery, state: FSMContext
):
    try:
        await callback.answer(text=LEXICON['right_answer_text'])
        data = await state.get_data()

        word_iter = data['word_iter']
        word_translations = data['word_translations']

        current_word = next(word_iter)

        translation, optionals = get_translation_optionals(
            word_translations, current_word
        )
        await callback.message.edit_text(
            text=LEXICON['training_text'].format(current_word),
            reply_markup=create_training_keyboard(
                translation, optionals
            )
        )
    except StopIteration:
        await callback.message.edit_text(
            text=LEXICON['no_more_words']
        )
        await state.clear()
    except Exception:
        logger.exception('Ошибка при обработки правильного ответа')


@router.callback_query(
    F.data == 'wrong_answer', StateFilter(Training.exists_training)
)
async def process_wrong_answer_press(callback: CallbackQuery):
    await callback.answer(text=LEXICON['wrong_answer_text'])


@router.callback_query(F.data == 'cancel_training', StateFilter(default_state))
async def process_cancel_training_press(
    callback: CallbackQuery, session: AsyncSession
):
    await callback.message.edit_text(text=LEXICON['cancel_training_text'])


@router.message(
    Command(commands=['beginning']), StateFilter(Training.exists_training)
)
async def process_beginning_with_training(message: Message):
    await message.answer(
        text=LEXICON['/beginning_with_training'],
        reply_markup=create_generic_keyboard('begin_new_training')
    )


@router.callback_query(
    F.data == 'end_training', StateFilter(Training.exists_training)
)
async def process_end_training_press(
    callback: CallbackQuery, state: FSMContext
):
    await state.clear()
    await callback.message.edit_text(
        text=LEXICON['end_training_text']
    )