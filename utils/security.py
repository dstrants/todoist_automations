import hmac
import base64

from fastapi import Request

from config.constants import TODOIST_CLIENT_SECRET as secret

async def todoist_validate_webhook_hmac(request: Request) -> bool:
    if not "X-Todoist-Hmac-SHA256" in request.headers:
        print("HMAC header not present on the request")
        return False

    if not secret:
        raise ValueError("TODOIST_CLIENT_SECRET not found in the provided configuration")

    body = await request.body()
    calculated_hmac = hmac.new(key=secret.encode(), msg=body, digestmod="sha256")
    hmac_digest = base64.b64encode(calculated_hmac.digest()).decode()

    if hmac_digest != (security_header := request.headers["X-Todoist-Hmac-SHA256"]):
        print(f"Digests do not much\n Calculated: {hmac_digest}\n Provided: {security_header}")
        return False

    return True