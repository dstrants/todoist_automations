from pydantic import BaseSettings, BaseModel


class TodoistConfig(BaseModel):
    client_id: str
    client_secret: str
    state_string: str
    priority_labels: str = "high,big,medium,quick"

    @property
    def priority_labels_set(self) -> set[str]:
        return set(self.priority_labels.split(","))


class MongoConfig(BaseModel):
    client: str

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


config = Config()