from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery


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
