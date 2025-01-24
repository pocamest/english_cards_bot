from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select

from database import User, UserWord, DefaultWord
import logging

logger = logging.getLogger(__name__)


async def _get_user(session: AsyncSession, tg_id: int):
    return await session.scalar(select(User).filter_by(tg_id=tg_id))


async def add_user(session: AsyncSession, user_name: str, tg_id: int):
    existing_user = await _get_user(session, tg_id)
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
