from collections.abc import Sequence
import json
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend import models, schemas, crud
from backend.services.quiz import quiz_service
from backend.utils import deps, redis

router = APIRouter()


@router.post("", response_model=schemas.QuizCreate, status_code=status.HTTP_201_CREATED)
async def create_bulk_quiz(
    quiz_in: schemas.QuizCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
    db: AsyncSession = Depends(deps.get_db),
) -> schemas.QuizCreate:
    return await quiz_service.create_bulk_quiz(quiz_in, db)


# TODO
@router.patch(
    "",
    response_model=schemas.QuizCreate,
    description="When task is running, you can't update it. \
        If you want to update it, you should stop it first.",
)
async def update_bulk_quiz(
    task_in: schemas.QuizCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
    db: AsyncSession = Depends(deps.get_db),
) -> schemas.QuizCreate:
    return await quiz_service.update_task(task_in, db)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    task_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> None:
    return await quiz_service.delete_quiz(task_id, db)


@router.get(
    "/{quiz_id}/detail",
    response_model=schemas.QuizBase,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def get_quiz_detail(
    quiz_id: int,
    page: int | None = None,
    per_page: int | None = None,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Sequence[models.Quiz]:
    if crud.user.is_superuser(current_user):
        return await quiz_service.get_questions_by_quiz_id(
            quiz_id=quiz_id, current_user=current_user, db=db
        )
    else:
        return await quiz_service.get_questions_by_quiz_id(
            quiz_id=quiz_id, current_user=current_user, db=db
        )


@router.get(
    "/{quiz_id}/apply",
    response_model=schemas.QuizCreate,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def apply_quiz(
    quiz_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Sequence[models.Quiz]:
    quiz: models.Quiz | None = await crud.quiz.get(id=quiz_id, db=db)

    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
        )

    current_user.quizzes.append(quiz)
    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    await quiz_service.set_questions_with_redis(
        quiz, quiz.question, current_user.id, quiz_id
    )

    return schemas.QuizCreate(quizzes=current_user.quizzes)


@router.post(
    "/{quiz_id}/select",
    response_model=schemas.QuizBase,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def select_question_choice(
    quiz_id: int,
    question_id: int,
    choice_user: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    key: str = f"user:{current_user.id},quiz_id:{quiz_id}"
    questions: str | None = redis.redis_client.get(key)
    if questions:
        questions = json.loads(questions)
        print("qqqq", questions)

        for question in questions.get("question"):
            if question.get("choice")[0].get("question_id") != question_id:
                continue
            question["choice_user"] = choice_user
    print("현재 상태", questions)

    redis.redis_client.set(key, json.dumps(questions))
    redis.redis_client.expire(key, 60 * 60 * 24)  # 1day
    return questions


@router.post(
    "/{quiz_id}/submit",
    response_model=schemas.QuizBase,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def submit_quiz(
    quiz_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    key: str = f"user:{current_user.id},quiz_id:{quiz_id}"
    questions: str = redis.redis_client.get(key)
    questions: list[dict] = json.loads(questions)
    score: int = 0

    for idx, question in enumerate(questions.get("question")):
        user_choice = question.get("choice_user")

        if user_choice is None:
            print(f"{idx + 1} 번 문제를 선택하지 않았습니다.")
            continue

        choice = question.get("choice")[user_choice - 1]
        if choice.get("is_answer"):
            score += 1
            print(f"{idx + 1} 번 문제에서 {user_choice} 을 골랐습니다.")
            print("정답")
        else:
            print("오답")

    print("score", score)
    return questions


@router.get(
    "",
    response_model=schemas.QuizCreate,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def get_quiz_handler(
    page: int = 1,
    per_page: int = 10,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
):
    if crud.user.is_superuser(user=current_user):
        quiz = await crud.quiz.get_list(db=db)
        return schemas.QuizCreate(quizzes=quiz)

    else:
        return schemas.QuizCreate(quizzes=current_user.quizzes)
