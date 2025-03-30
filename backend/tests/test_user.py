# type: ignore
import pytest

from backend import crud
from backend.utils.security import get_password_hash

PATH = "/api/v1/users"


@pytest.mark.asyncio
async def test_get_user(init):
    _, client = init
    response = await client.get(PATH + "/1")
    assert response.status_code == 200
    assert response.json()["username"] == "user1@user1.com"


@pytest.mark.asyncio
async def test_update_password(init):
    db, client = init
    response = await client.patch(PATH + "/1", json={"password": "user1_password2"})
    user = await crud.user.get(db, id=1)
    assert response.status_code == 200
    assert user.password != get_password_hash("user1_password")


@pytest.mark.asyncio
async def test_delete_user(init):
    db, client = init
    response = await client.delete(PATH + "/1", headers={"password": "user1_password"})
    user = await crud.user.get(db, id=1)
    assert response.status_code == 204
    assert user is None


@pytest.mark.asyncio
async def test_delete_user_with_wrong_password(init):
    db, client = init
    response = await client.delete(PATH + "/1", headers={"password": "wrong_password"})
    user = await crud.user.get(db, id=1)
    assert response.status_code == 401
    assert user is not None


@pytest.mark.asyncio
async def test_get_user_me(init):
    _, client = init
    response = await client.get(PATH + "/me")
    assert response.status_code == 200
    assert response.json()["username"] is not None
