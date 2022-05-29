import hmac
import base64

from fastapi import Request

from config.base import config

async def todoist_validate_webhook_hmac(request: Request) -> bool:
    if not "X-Todoist-Hmac-SHA256" in request.headers:
        print("HMAC header not present on the request")
        return False

    body = await request.body()
    calculated_hmac = hmac.new(key=config.todoist.client_secret_encoded, msg=body, digestmod="sha256")
    hmac_digest = base64.b64encode(calculated_hmac.digest()).decode()

    if hmac_digest != (security_header := request.headers["X-Todoist-Hmac-SHA256"]):
        print(f"Digests do not much\n Calculated: {hmac_digest}\n Provided: {security_header}")
        return False

    return True