from pydantic import BaseModel


class TelegramLogin(BaseModel):
    phone: str
    email: str