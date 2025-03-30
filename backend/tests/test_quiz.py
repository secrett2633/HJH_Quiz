# type: ignore
import pytest
import pytest_asyncio

from backend import crud, schemas
from backend.services.quiz import quiz_service
from backend.utils.security import get_password_hash

PATH = "/api/v1/quiz"


@pytest_asyncio.fixture()
async def init_for_quiz(init_with_superuser):
    db, client = init_with_superuser
    quiz_in = schemas.QuizCreate(
        name="test",
        limit=10,
        status="order",
        question=[
            schemas.QuestionCreate(
                name="주어진 숫자 중 짝수를 모두 고르세요.",
                choice=[
                    schemas.ChoiceBase(name="2", is_answer=True),
                    schemas.ChoiceBase(name="10", is_answer=True),
                    schemas.ChoiceBase(name="1", is_answer=False),
                ],
            ),
            schemas.QuestionCreate(
                name="다음 중 계절의 이름으로 옳은 것을 고르세요.",
                choice=[
                    schemas.ChoiceBase(name="여름", is_answer=True),
                    schemas.ChoiceBase(name="달", is_answer=False),
                    schemas.ChoiceBase(name="바람", is_answer=False),
                ],
            ),
            schemas.QuestionCreate(
                name="대한민국의 수도는 어디인가요?",
                choice=[
                    schemas.ChoiceBase(name="서울", is_answer=True),
                    schemas.ChoiceBase(name="부산", is_answer=False),
                    schemas.ChoiceBase(name="대구", is_answer=False),
                ],
            ),
        ],
    )

    await quiz_service.create_quiz(db=db, quiz_in=quiz_in)

    yield db, quiz_in, client


@pytest.mark.asyncio
async def test_create_quiz(init_for_quiz):
    db, quiz_in, client = init_for_quiz

    response = await client.post(PATH, json=quiz_in.dict())

    assert response.status_code == 201
    assert response.json()["name"] == "test"
    assert response.json()["status"] == "order"
    assert response.json()["limit"] == 10
    assert len(response.json()["question"]) == 3
    assert len(response.json()["question"][0]["choice"]) == 3


@pytest.mark.asyncio
async def test_get_quiz(init_for_quiz):
    db, quiz_in, client = init_for_quiz

    response = await client.get(PATH)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "test"
    assert response.json()[0]["status"] == "order"
    assert response.json()[0]["limit"] == 10


@pytest.mark.asyncio
async def test_update_quiz(init_for_quiz):
    db, _, client = init_for_quiz

    quiz_in = schemas.QuizBase(
        name="test1",
        limit=100,
        status="random",
    )

    response = await client.patch(PATH + "/1", json=quiz_in.dict())
    assert response.status_code == 200
    assert response.json()["name"] == "test1"
    assert response.json()["status"] == "random"
    assert response.json()["limit"] == 100


@pytest.mark.asyncio
async def test_update_question(init_for_quiz):
    db, _, client = init_for_quiz

    question_in = schemas.QuestionUpdate(
        id=1,
        name="test1",
        choice=[
            schemas.ChoiceUpdate(id=1, name="1111", is_answer=True),
            schemas.ChoiceUpdate(id=2, name="2222", is_answer=True),
            schemas.ChoiceUpdate(id=3, name="3333", is_answer=False),
        ],
    )

    response = await client.patch(PATH + "/1/question", json=question_in.dict())
    assert response.json()["name"] == "test1"
    assert len(response.json()["choice"]) == 3


@pytest.mark.asyncio
async def test_get_quiz_detail(init_for_quiz):
    db, quiz_in, client = init_for_quiz

    response = await client.get(PATH + "/1/detail")
    assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_create_quiz(init):
#     _, client = init
#     response = await client.post(PATH, json={})
#
#
#
#
#
#
# @pytest.mark.asyncio
# async def test_update_password(init):
#     db, client = init
#     response = await client.patch(PATH + "/1", json={"password": "user1_password2"})
#     user = await crud.user.get(db, id=1)
#     assert response.status_code == 200
#     assert user.password != get_password_hash("user1_password")
#
#
# @pytest.mark.asyncio
# async def test_delete_user(init):
#     db, client = init
#     response = await client.delete(PATH + "/1", headers={"password": "user1_password"})
#     user = await crud.user.get(db, id=1)
#     assert response.status_code == 204
#     assert user is None
#
#
# @pytest.mark.asyncio
# async def test_delete_user_with_wrong_password(init):
#     db, client = init
#     response = await client.delete(PATH + "/1", headers={"password": "wrong_password"})
#     user = await crud.user.get(db, id=1)
#     assert response.status_code == 401
#     assert user is not None
#
#
# @pytest.mark.asyncio
# async def test_get_user_me(init):
#     _, client = init
#     response = await client.get(PATH + "/me")
#     assert response.status_code == 200
#     assert response.json()["username"] is not None
