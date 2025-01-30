from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
import re


# Подумать над дублированием кода
class IsPage(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, int] | bool:
        if not callback.data:
            return False

        parts = callback.data.split(':', 1)
        if len(parts) != 2:
            return False

        name, page = parts
        if name == 'page' and page.isdigit():
            return {'page': int(page)}

        else:
            return False


class IsDeleteWord(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, str] | bool:
        if not callback.data:
            return False

        parts = callback.data.split(':', 1)
        if len(parts) != 2:
            return False

        name, word = parts
        if name == 'del':
            return {'word': word}

        else:
            return False


class IsCorrectWord(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, str] | bool:
        word = message.text.strip()
        if word and bool(re.fullmatch(r'^[А-Яа-яёЁ- ]+$', word)):
            return {'word': word.lower()}
        else:
            return False


class IsCorrectTranslation(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, str] | bool:
        translation = message.text.strip()
        if translation and bool(re.fullmatch(r"^[A-Za-z'- ]+$", translation)):
            return {'translation': translation.lower()}
        else:
            return False
