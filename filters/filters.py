from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession
from database import word_exists
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

        return False


class IsCorrectWord(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, str] | bool:
        word = message.text.strip()
        if word and bool(re.fullmatch(r'^[А-Яа-яёЁ -]+$', word)):
            return {'word': word.lower()}
        return False


class IsWordNotExists(BaseFilter):
    async def __call__(
        self, message: Message, session: AsyncSession
    ) -> dict[str, str] | bool:
        word = message.text.strip()
        tg_id = message.from_user.id
        flag = await word_exists(session, tg_id, word)
        if flag:
            return False
        return True


class IsCorrectTranslation(BaseFilter):
    async def __call__(self, message: Message) -> dict[str, str] | bool:
        translation = message.text.strip()
        if translation and bool(re.fullmatch(r"^[A-Za-z' -]+$", translation)):
            return {'translation': translation.lower()}
        return False
