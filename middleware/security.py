from fastapi.security.api_key import APIKeyHeader
from fastapi import Security, status, HTTPException

from config.base import config

api_key_header = APIKeyHeader(name="X-DOISTER-API-KEY", auto_error=True)


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    """Validates the incoming api key and returns the api key if valid"""
    if api_key == config.api_key:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not authenticate user"
    )
