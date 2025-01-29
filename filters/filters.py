from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
import re


class IsPage(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, int] | bool:
        if not callback.data:
            return False

        name, page = callback.data.split(':')
        if name == 'page' and page.isdigit():
            return {'page': int(page)}

        else:
            return False


class IsDeleteWord(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> dict[str, str] | bool:
        if not callback.data:
            return False

        name, word = callback.data.split(':')
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
