from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from sqlalchemy import String, BigInteger, ForeignKey
from database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_name: Mapped[str] = mapped_column(String(255))
    tg_id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True
    )

    user_words: Mapped[list['UserWord']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )
    user_ignored_words: Mapped[list['UserIgnoredWord']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (
            f'User(id={self.id}, user_name={self.user_name!r},'
            f' tg_id={self.tg_id})'
        )


class UserWord(Base):
    __tablename__ = 'user_words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    translation: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )

    user: Mapped['User'] = relationship(
        back_populates='user_words'
    )

    def __repr__(self):
        return (
            f'UserWord(id={self.id}, word={self.word!r},'
            f'translation={self.translation!r})'
        )


class DefaultWord(Base):
    __tablename__ = 'default_words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True
    )
    translation: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    user_ignored_words: Mapped[list['UserIgnoredWord']] = relationship(
        back_populates='default_word',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return (
            f'DefaultWord(id={self.id}, word={self.word!r},'
            f'translation={self.translation!r})'
        )


class UserIgnoredWord(Base):
    __tablename__ = 'user_ignored_words'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False
    )
    word_id: Mapped[int] = mapped_column(
        ForeignKey('default_words.id'), nullable=False
    )

    user: Mapped['User'] = relationship(
        back_populates='user_ignored_words'
    )
    default_word: Mapped['DefaultWord'] = relationship(
        back_populates='user_ignored_words'
    )

    def __repr__(self):
        return (
            f'UserIgnoredWord(id={self.id}, '
            f'user_id={self.user_id}, word_id={self.word_id})'
        )
