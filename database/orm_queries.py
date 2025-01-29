from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import union_all

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
        except SQLAlchemyError as e:
            await session.rollback()
            logger.exception(
                f'Ошибка при добавлении пользователя {user_name!r},'
                f' tg_id={tg_id}: {e}'
            )


async def add_default_words(
    session: AsyncSession, word_pairs: list[dict[str, str]]
):
    try:
        default_words = [DefaultWord(**word_pair) for word_pair in word_pairs]
        session.add_all(default_words)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        logger.exception(
            f'Ошибка при добавлении карточек по умолчанию: {e}'
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
            .filter(UserIgnoredWord.id == None)
        )
        union_query = union_all(user_words_query, default_words_query)
        result = await session.execute(union_query)
        result_list = result.fetchall()
        random.shuffle(result_list)
        return dict(result_list)
    except SQLAlchemyError as e:
        logger.exception(f'Ошибка при выполнении запроса к базе данных: {e}')
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
    except SQLAlchemyError as e:
        logger.exception(f'Ошибка при удаления слова, {e}')
        await session.rollback()
