from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from backend.utils.validator import PhoneNumber


class UserCreate(BaseModel):
    username: EmailStr
    password: str
    phone_number: PhoneNumber = Field(..., example="+82 010-1111-1111")


class UserUpdate(BaseModel):
    password: str | None = None
    phone_number: PhoneNumber | None = Field(default=None, example="+82 010-1111-1111")
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class UserInDB(BaseModel):
    id: int
    username: EmailStr
    phone_number: PhoneNumber = Field(..., example="+82 010-1111-1111")
    first_name: str | None = None
    last_name: str | None = None
    created: datetime
    updated: datetime | None = None
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True
