# type: ignore
import pytest

PATH = "/api/v1/auth"


@pytest.mark.asyncio
async def test_signup(init_without_token):
    data, client = init_without_token
    response = await client.post(PATH + "/signup", json=data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_signin(init_without_token):
    data, client = init_without_token
    await client.post(PATH + "/signup", json=data)
    response = await client.post(PATH + "/signin", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert "user" in response.json()


@pytest.mark.asyncio
async def test_signin_wrong_credentials(init_without_token):
    data, client = init_without_token
    response = await client.post(PATH + "/signin", data=data)
    assert response.status_code == 401
