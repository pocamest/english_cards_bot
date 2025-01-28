from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon import LEXICON


def create_cards_keyboard(
    word_translations: dict[str, str],
    page: int = 0, limit: int = 10
) -> InlineKeyboardMarkup:

    start = page * limit
    end = start + limit
    pagination_words = sorted(word_translations.items())[start:end]

    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(
        *[InlineKeyboardButton(
            text=f'{word} - {translation}',
            callback_data=f'del:{word}'
        ) for word, translation in pagination_words
        ],
        width=1
    )

    pagination_buttons = []
    if page > 0:
        pagination_buttons.append(
            InlineKeyboardButton(
                text=LEXICON['backward'], callback_data=f'page:{page-1}'
            )
        )
    if end < len(word_translations):
        pagination_buttons.append(
            InlineKeyboardButton(
                text=LEXICON['forward'], callback_data=f'page:{page+1}'
            )
        )
    kb_builder.row(*pagination_buttons)

    return kb_builder.as_markup()
