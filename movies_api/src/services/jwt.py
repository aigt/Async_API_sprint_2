import logging
from jose import jwt

from fastapi import Depends, Security
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials

from core.config import get_settings

settings = get_settings()
bearer = HTTPBearer(auto_error=False)


async def get_token(auth_credentials: HTTPAuthorizationCredentials = Security(bearer)) -> str | None:
    if not auth_credentials:
        return None
    token = auth_credentials.credentials
    return token


async def decode_token_payload(token: str | None = Depends(get_token)) -> dict:
    if token is None:
        return None
    return jwt.decode(token, settings.auth_rsa_public_key, "RS256")


async def is_subscriber(token_payload: dict | None = Depends(decode_token_payload)) -> bool:
    logging.debug(f'{token_payload=}')
    if token_payload is None:
        return False
    roles = token_payload.get('roles', '').split()
    if settings.subscriber_role_name in roles:
        return True
    return False
