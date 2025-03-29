from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend import schemas
from backend.schemas.auth import UserTokenData
from backend.services.auth import auth_service
from backend.utils import deps

router = APIRouter()


@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user_in: schemas.UserCreate, db: AsyncSession = Depends(deps.get_db)
) -> None:
    return await auth_service.signup(db, user_in)


@router.post("/signin", response_model=UserTokenData)
async def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(deps.get_db),
) -> UserTokenData:
    return await auth_service.signin(db, form_data)
