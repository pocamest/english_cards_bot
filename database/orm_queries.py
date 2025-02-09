from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import union_all, delete

from database import User, UserWord, DefaultWord, UserIgnoredWord
import logging
import random

logger = logging.getLogger(__name__)


async def add_user(session: AsyncSession, user_name: str, tg_id: int):
    existing_user = await session.scalar(select(User).filter_by(tg_id=tg_id))
    if existing_user:
        logger.info(f"Пользователь с tg_id={tg_id} уже существует.")
    else:
        new_user = User(user_name=user_name, tg_id=tg_id)
        try:
            session.add(new_user)
            await session.commit()
            logger.debug(f'Добавлен пользователь {new_user!r}')
        except SQLAlchemyError:
            await session.rollback()
            logger.exception(
                f'Ошибка при добавлении пользователя {user_name!r},'
                f' tg_id={tg_id}'
            )


async def get_all_words(session: AsyncSession, tg_id: int):
    try:
        user_query = select(User.id).filter_by(tg_id=tg_id)
        user_id = await session.scalar(user_query)

        user_words_query = (
            select(UserWord.word, UserWord.translation)
            .filter_by(user_id=user_id)
        )
        default_words_query = (
            select(DefaultWord.word, DefaultWord.translation)
            .outerjoin(
                UserIgnoredWord,
                (DefaultWord.id == UserIgnoredWord.word_id) &
                (UserIgnoredWord.user_id == user_id)
            )
            .filter(UserIgnoredWord.id.is_(None))
        )
        union_query = union_all(user_words_query, default_words_query)
        result = await session.execute(union_query)
        result_list = result.fetchall()
        random.shuffle(result_list)
        return dict(result_list)
    except SQLAlchemyError:
        logger.exception('Ошибка при выполнении запроса к базе данных')
        return {}


async def delete_word(session: AsyncSession, tg_id: int, word: str):
    try:
        user_word_to_delete = await session.scalar(
            select(UserWord)
            .join(User, UserWord.user_id == User.id)
            .filter(User.tg_id == tg_id, UserWord.word == word)
        )
        if user_word_to_delete:
            await session.delete(user_word_to_delete)
            await session.commit()
            return

        default_word_to_delete = await session.scalar(
            select(DefaultWord)
            .filter(DefaultWord.word == word)
        )
        user_id = await session.scalar(
            select(User.id).filter(User.tg_id == tg_id)
        )
        user_ignored_word = UserIgnoredWord(
            user_id=user_id,
            word_id=default_word_to_delete.id
        )
        session.add(user_ignored_word)
        await session.commit()
    except SQLAlchemyError:
        logger.exception('Ошибка при удаления слова')
        await session.rollback()


# потом переделать
async def word_exists(session: AsyncSession, tg_id: int, word: str):
    try:
        user_id = await session.scalar(
            select(User.id).filter(User.tg_id == tg_id)
        )

        user_words_query = (
            select(UserWord.word)
            .filter(UserWord.user_id == user_id, UserWord.word == word)
        )

        default_words_query = (
            select(DefaultWord.word)
            .outerjoin(
                UserIgnoredWord,
                (DefaultWord.id == UserIgnoredWord.word_id) &
                (UserIgnoredWord.user_id == user_id)
            )
            .filter(
                DefaultWord.word == word,
                UserIgnoredWord.id.is_(None)
            )
        )

        union_query = union_all(user_words_query, default_words_query)
        result = await session.scalar(select(union_query.exists()))

        return bool(result)
    except SQLAlchemyError:
        logger.exception(f'Ошибка при проверки наличия слова {word}')
        return False


async def add_card(
    session: AsyncSession, tg_id: int,
    word: str, translation: str
):
    try:
        user_id = await session.scalar(
            select(User.id).filter(User.tg_id == tg_id)
        )
        user_word = UserWord(
            word=word,
            translation=translation,
            user_id=user_id
        )
        session.add(user_word)
        await session.commit()

    except SQLAlchemyError:
        await session.rollback()
        logger.exception(f'Ошибка при добавления слова {word}')


async def clear_user_changes(
    session: AsyncSession, tg_id: int
):
    try:
        user_id = await session.scalar(
            select(User.id).filter(User.tg_id == tg_id)
        )

        await session.execute(
            delete(UserWord).where(UserWord.user_id == user_id)
        )
        await session.execute(
            delete(UserIgnoredWord).where(UserIgnoredWord.user_id == user_id)
        )

        await session.commit()

    except SQLAlchemyError:
        await session.rollback()
        logger.exception(
            'Ошибка при удалении пользовательских изменений'
        )
