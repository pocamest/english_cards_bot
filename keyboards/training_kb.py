from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random


def create_training_keyboard(
    translation: str, optionals: list[str]
) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    translation_button = InlineKeyboardButton(
        text=translation,
        callback_data='right_answer'
    )
    optionals_buttons: list[InlineKeyboardButton] = [
        InlineKeyboardButton(
            text=optional,
            callback_data='wrong_answer'
        ) for optional in optionals
    ]
    optionals_buttons.append(translation_button)
    random.shuffle(optionals_buttons)
    kb_builder.row(*optionals_buttons, width=2)
    return kb_builder.as_markup()
