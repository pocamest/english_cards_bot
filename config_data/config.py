from dataclasses import dataclass
from environs import Env


@dataclass
class DataBaseConfig:
    url: str


@dataclass
class TgBot:
    token: str


@dataclass
class Config:
    db: DataBaseConfig
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        db=DataBaseConfig(
            url=env('DB_URL')
        ),
        tg_bot=TgBot(
            token=env('BOT_TOKEN')
        )
    )
