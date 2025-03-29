from pydantic import BaseModel

from backend.schemas.user import UserInDB


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    exp: int | None = None
    sub: int | None = None


class UserTokenData(BaseModel):
    access_token: str
    token_type: str
    user: UserInDB
