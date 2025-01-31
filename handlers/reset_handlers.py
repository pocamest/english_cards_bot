from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from lexicon import LEXICON

from database import clear_user_changes

from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import create_generic_keyboard

import logging

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command(commands=['reset']))
async def process_clear(message: Message):
    await message.answer(
        text=LEXICON['/reset'],
        reply_markup=create_generic_keyboard(
            'reset_changes', 'cancel_reset'
        )
    )


@router.callback_query(F.data == 'reset_changes')
async def process_reset_changes_press(
    callback: CallbackQuery, session: AsyncSession
):
    tg_id = callback.from_user.id
    await clear_user_changes(session, tg_id)
    await callback.message.edit_text(
        text=LEXICON['reset_changes_text']
    )


@router.callback_query(F.data == 'cancel_reset')
async def process_cancel_reset_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['cancel_reset_text']
    )
