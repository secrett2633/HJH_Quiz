from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend import models, schemas
from backend.services.user import user_service
from backend.utils import deps

router = APIRouter()


@router.get("/me", response_model=schemas.UserInDB)
async def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> models.User:
    return current_user


@router.get("/{user_id}", response_model=schemas.UserInDB)
async def read_user(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> models.User:
    return await user_service.read_user(user_id, current_user, db)


@router.patch("/{user_id}", response_model=schemas.UserInDB)
async def update_user(
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> models.User:
    return await user_service.update_user(user_id, user_in, current_user, db)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    request: Request,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> None:
    return await user_service.delete_user(user_id, request, current_user, db)
