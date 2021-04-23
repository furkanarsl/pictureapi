from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str


class TokenPayload(BaseModel):
    sub: Optional[str]
    iat: Optional[str]
    nbf: Optional[str]
    jti: Optional[str]
    exp: Optional[str]
    type: Optional[str]


class LoginToken(BaseModel):
    access_token: str
    refresh_token: str

