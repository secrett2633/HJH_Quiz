from fastapi import HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud, models, schemas
from backend.utils.security import verify_password


class UserService:
    @staticmethod
    async def read_user(
        user_id: int,
        current_user: models.User,
        db: AsyncSession,
    ) -> models.User:
        if user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user = await crud.user.get(db, id=user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return user

    @staticmethod
    async def update_user(
        user_id: int,
        user_in: schemas.UserUpdate,
        current_user: models.User,
        db: AsyncSession,
    ) -> models.User:
        user = await UserService.read_user(user_id, current_user, db)

        return await crud.user.update(db, db_obj=user, obj_in=user_in)

    @staticmethod
    async def delete_user(
        user_id: int,
        request: Request,
        current_user: models.User,
        db: AsyncSession,
    ) -> None:
        user = await UserService.read_user(user_id, current_user, db)

        password = request.headers.get("password", "no password")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        await crud.user.delete(db, id=user_id)

        return


user_service = UserService()
