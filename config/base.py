import logging
from typing import Optional

from github import Github
from pyairtable.api.table import Table
from pydantic import BaseModel, BaseSettings
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.mongo_client import MongoClient


class TodoistConfig(BaseModel):
    """Todoist configuration."""
    client_id: str
    client_secret: str
    state_string: str
    priority_labels: str = "huge,big,medium,quick"
    oauth_base_url: str = "https://todoist.com/oauth/authorize"
    oauth_scope: str = "data:read_write,data:delete"

    @property
    def priority_labels_set(self) -> set[str]:
        """Builds a set of priority labels."""
        return set(self.priority_labels.split(","))

    @property
    def client_secret_encoded(self) -> bytes:
        """Encodes the client secret."""
        return self.client_secret.encode()

    @property
    def oauth_full_url(self) -> str:
        """Builds the full oauth url."""
        return f"{self.oauth_base_url}?client_id={self.client_id}&scope={self.oauth_scope}&state={self.state_string}"


class MongoConfig(BaseModel):
    """MongoDB configuration"""
    server: str
    timeout: int = 30_000
    todoist_database_name: str = "todoist"
    # NOTE: This is a placeholder for the future.
    telegram_database_name: str = "telegram"
    tools_database_name: str = "tools"

    @property
    def client(self) -> MongoClient:
        """Initializes a MongoClient."""
        return MongoClient(self.server, serverSelectionTimeoutMS=self.timeout)

    @property
    def todoist_database(self) -> Database:
        """Returns the todoist database."""
        return self.client[self.todoist_database_name]

    @property
    def telegram_database(self) -> Database:
        """Returns the telegram database."""
        return self.client[self.telegram_database_name]

    @property
    def tools_database(self) -> Database:
        """Returns the tools database."""
        return self.client[self.tools_database_name]

    def todoist_collection(self, collection: str = "items") -> Collection:
        """Returns the todoist collection."""
        return self.todoist_database[collection]

    def telegram_collection(self, collection: str = "authentication_codes") -> Collection:
        """Returns the telegram collection."""
        return self.telegram_database[collection]

    def tools_collection(self, collection: str = "tools") -> Collection:
        """Returns the tools collection."""
        return self.tools_database[collection]


class TelegramConfig(BaseModel):
    """Telegram bot configuration."""
    bot_token: str
    bot_name: str


class SentryConfig(BaseModel):
    """Sentry configuration."""
    dsn: Optional[str] = None
    traces_sample_rate: float = 1.0


class AirtableConfig(BaseModel):
    """Airtable configuration."""
    token: str
    base_id: str
    cache: bool = True
    table_name: str = "Tools"

    @property
    def base(self) -> Table:
        """Returns the tools airtable base."""
        return Table(self.token, self.base_id, self.table_name)


class GithubConfig(BaseModel):
    """Github configuration."""
    token: str | None = None

    @property
    def client(self) -> Github:
        """Returns the github client."""
        return Github(self.token)


class Config(BaseSettings):
    """
    This is the base config class.

    It is used to configure the various components of the application.
    """
    airtable: AirtableConfig
    todoist: TodoistConfig
    mongo: MongoConfig
    telegram: TelegramConfig
    sentry: SentryConfig = SentryConfig()
    github: GithubConfig = GithubConfig()

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
        """Exposes a common logger for the application."""
        logging.basicConfig(level=self.log_level)
        return logging.getLogger("doister")


# Configuration is initialized so that it can be used in other modules.
config = Config()
