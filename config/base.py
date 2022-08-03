import logging
from typing import Optional

from pydantic import BaseModel, BaseSettings
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient


class TodoistConfig(BaseModel):
    client_id: str
    client_secret: str
    state_string: str
    priority_labels: str = "huge,big,medium,quick"
    oauth_base_url: str = "https://todoist.com/oauth/authorize"
    oauth_scope: str = "data:read_write,data:delete"

    @property
    def priority_labels_set(self) -> set[str]:
        return set(self.priority_labels.split(","))

    @property
    def client_secret_encoded(self) -> bytes:
        return self.client_secret.encode()

    @property
    def oauth_full_url(self) -> str:
        return f"{self.oauth_base_url}?client_id={self.client_id}&scope={self.oauth_scope}&state={self.state_string}"


class MongoConfig(BaseModel):
    server: str
    todoist_database_name: str = "todoist"
    # NOTE: This is a placeholder for the future.
    telegram_database_name: str = "telegram"

    @property
    def client(self) -> MongoClient:
        return MongoClient(self.server)

    @property
    def todoist_database(self) -> Database:
        return self.client[self.todoist_database_name]

    @property
    def telegram_database(self) -> Database:
        return self.client[self.telegram_database_name]

    def todoist_collection(self, collection: str = "items") -> Collection:
        return self.todoist_database[collection]

    def telegram_collection(self, collection: str = "authentication_codes") -> Collection:
        return self.telegram_database[collection]


class TelegramConfig(BaseModel):
    bot_token: str
    bot_name: str


class SentryConfig(BaseModel):
    dsn: Optional[str] = None
    traces_sample_rate: float = 1.0


class Config(BaseSettings):
    todoist: TodoistConfig
    mongo: MongoConfig
    telegram: TelegramConfig
    sentry: SentryConfig = SentryConfig()

    timezone: str = "Europe/Athens"
    host: str = "http://localhost:8000"

    log_level: str = "INFO"
    env: str = "dev"

    class Config:
        env_prefix = "DOISTER_"
        env_nested_delimiter = '__'

    @property
    def logger(self) -> logging.Logger:
        logging.basicConfig(level=self.log_level)
        return logging.getLogger("doister")


config = Config()
