from jose import jwt

from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

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
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


async def require_jwt(token: str = Depends(get_token)) -> dict:
    return jwt.decode(token, settings.auth_rsa_public_key, "RS256")
