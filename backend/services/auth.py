from datetime import timedelta

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud, schemas
from backend.core.config import settings
from backend.utils import security


class AuthService:
    @staticmethod
    async def signup(db: AsyncSession, user_in: schemas.UserCreate) -> None:
        if await crud.user.get_by_username(db, username=user_in.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        await crud.user.create(db, obj_in=user_in)
        return

    @staticmethod
    async def signin(
        db: AsyncSession, form_data: OAuth2PasswordRequestForm
    ) -> schemas.UserTokenData:
        user = await crud.user.authenticate(
            db, username=form_data.username, password=form_data.password
        )

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        return schemas.UserTokenData(
            access_token=security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            token_type=settings.TOKEN_TYPE,
            user=schemas.UserInDB.from_orm(user),
        )


auth_service = AuthService()
