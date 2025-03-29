# type: ignore
import asyncio
from datetime import timedelta

import pytest_asyncio
from httpx import AsyncClient

from backend import crud
from backend.core.session import engine
from backend.main import app
from backend.models import Base
from backend.schemas import UserCreate
from backend.utils import security
from backend.utils.deps import get_db


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture()
async def db():
    db = None
    try:
        async for db in get_db():
            assert db.bind.url.database == "test_db"

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        async for db in get_db():
            yield db
    finally:
        if db is not None:
            await db.close()


@pytest_asyncio.fixture(scope="function")
async def init(db):
    user_in = UserCreate(
        username="user1@user1.com",
        password="user1_password",
        phone_number="+82 010-1111-1111",
    )
    user = await crud.user.create(db, obj_in=user_in)
    access_token = security.create_access_token(
        user.id, expires_delta=timedelta(minutes=600)
    )
    async with AsyncClient(
        app=app,
        base_url="http://testserver",
        headers={"Authorization": f"Bearer {access_token}"},
    ) as client:
        yield db, client


@pytest_asyncio.fixture(scope="function")
async def init_without_token(db):
    data = {
        "username": "user1@user1.com",
        "password": "user1_password",
        "phone_number": "+82 010-1111-1111",
    }
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield data, client
