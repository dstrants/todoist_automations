from pydantic import BaseModel


class TelegramLogin(BaseModel):
    phone: str
    email: str


class TelegramLoginCallback(BaseModel):
    phone: str
    code: str
    email: str