from utils.telegram import get_telegram_client

async def telegram_send_text(message: str, phone: str) -> None:
    """
    Sends a text message through Telegram bot.
    """
    client = get_telegram_client()
    await client.connect()

    if not client.is_user_authorized():
        raise ValueError(f"Telegram bot is not authorized to send message to phone number {phone}.")

    await client.send_message(phone, message)  # type: ignore

    client.disconnect()


async def telegram_send_authorization_code_to_user(phone: str) -> None:
    """
    Authorizes a Telegram user.
    """
    client = get_telegram_client()
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        client.disconnect()


async def validate_telegram_authorization_code(phone: str, code: str) -> None:
    """
    Validates a Telegram authorization code.
    """
    client = get_telegram_client()
    await client.connect()

    if not client.is_user_authorized():
        await client.sign_in(phone, code)
        client.disconnect()
        print("Phone validation for {phone} was successful.")