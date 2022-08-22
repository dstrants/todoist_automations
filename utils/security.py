import base64
import hmac

from fastapi import Request

from config.base import config


# TODO: This should be moved to security middleware module
async def todoist_validate_webhook_hmac(request: Request) -> bool:
    """Performs a validation of the todoist webhook hmac."""
    if "X-Todoist-Hmac-SHA256" not in request.headers:
        config.logger.warning("Missing X-Todoist-Hmac-SHA256 header")
        return False

    body = await request.body()
    calculated_hmac = hmac.new(key=config.todoist.client_secret_encoded, msg=body, digestmod="sha256")
    hmac_digest = base64.b64encode(calculated_hmac.digest()).decode()

    if hmac_digest != request.headers["X-Todoist-Hmac-SHA256"]:
        config.logger.warning("Invalid X-Todoist-Hmac-SHA256 header")
        return False

    return True
