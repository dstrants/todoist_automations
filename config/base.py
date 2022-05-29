import logging

from pydantic import BaseSettings, BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

class TodoistConfig(BaseModel):
    client_id: str
    client_secret: str
    state_string: str
    priority_labels: str = "high,big,medium,quick"

    @property
    def priority_labels_set(self) -> set[str]:
        return set(self.priority_labels.split(","))

    @property
    def client_secret_encoded(self) -> bytes:
        return self.client_secret.encode()


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


class Config(BaseSettings):
    todoist: TodoistConfig
    mongo: MongoConfig
    telegram: TelegramConfig

    timezone: str = "Europe/Athens"
    host: str = "http://localhost:8000"

    class Config:
        env_prefix = "DOISTER_"
        env_nested_delimiter = '__'

    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger("doister")


config = Config()