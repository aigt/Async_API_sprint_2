from jose import jwt

from fastapi import Request, Depends

from core.config import get_settings

settings = get_settings()


def get_authorization_scheme_param(authorization_header_value: str) -> tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


async def get_token(request: Request) -> str | None:
    authorization: str = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)
    if not authorization or scheme.lower() != "bearer":
        return None
    return token


async def decode_token_payload(token: str | None = Depends(get_token)) -> dict:
    if token is None:
        return None
    return jwt.decode(token, settings.auth_rsa_public_key, "RS256")


async def is_subscriber(token_payload: dict = Depends(decode_token_payload)) -> bool:
    if token_payload is None:
        return False
    roles = token_payload.get('roles', '').split()
    if settings.subscriber_role_name in roles:
        return True
    return False
