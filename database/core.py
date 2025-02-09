from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DataBase:
    def __init__(self, url: str) -> None:
        self.engine = create_async_engine(url, echo=True)
        self.session_factory = async_sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False
        )

