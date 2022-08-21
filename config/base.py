import logging
from typing import Optional

from pyairtable.api.table import Table
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
    timeout: int = 30_000
    todoist_database_name: str = "todoist"
    # NOTE: This is a placeholder for the future.
    telegram_database_name: str = "telegram"
    tools_database_name: str = "tools"

    @property
    def client(self) -> MongoClient:
        return MongoClient(self.server, serverSelectionTimeoutMS=self.timeout)

    @property
    def todoist_database(self) -> Database:
        return self.client[self.todoist_database_name]

    @property
    def telegram_database(self) -> Database:
        return self.client[self.telegram_database_name]

    @property
    def tools_database(self) -> Database:
        return self.client[self.tools_database_name]

    def todoist_collection(self, collection: str = "items") -> Collection:
        return self.todoist_database[collection]

    def telegram_collection(self, collection: str = "authentication_codes") -> Collection:
        return self.telegram_database[collection]

    def tools_collection(self, collection: str = "tools") -> Collection:
        return self.tools_database[collection]


class TelegramConfig(BaseModel):
    bot_token: str
    bot_name: str


class SentryConfig(BaseModel):
    dsn: Optional[str] = None
    traces_sample_rate: float = 1.0


class AirtableConfig(BaseModel):
    token: str
    base_id: str
    cache: bool = True
    table_name: str = "Tools"

    @property
    def base(self) -> Table:
        return Table(self.token, self.base_id, self.table_name)


class Config(BaseSettings):
    airtable: AirtableConfig
    todoist: TodoistConfig
    mongo: MongoConfig
    telegram: TelegramConfig
    sentry: SentryConfig = SentryConfig()

    api_key: str

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
