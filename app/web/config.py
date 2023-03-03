import typing
from dataclasses import dataclass

import yaml

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class TelegramBotConfig:
    token: str


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "wheel_of_fortune"

    @property
    def url(self):
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig = None
    bot: TelegramBotConfig = None
    database: DatabaseConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        bot=TelegramBotConfig(
            token=raw_config["telegram"]["bot_token"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
    )


def get_database_config(config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)
    return DatabaseConfig(**raw_config["database"])
