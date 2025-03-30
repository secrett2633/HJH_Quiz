from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from redis import Redis

from backend import models, schemas, crud
from backend.services.question import question_service
from backend.services.quiz import quiz_service
from backend.utils import deps

router = APIRouter()


@router.post(
    "",
    response_model=schemas.QuizUpdate,
    status_code=status.HTTP_201_CREATED,
    description="Create a new quiz",
)
async def create_quiz(
    quiz_in: schemas.QuizCreate,
    _: models.User = Depends(deps.get_current_active_superuser),
    db: AsyncSession = Depends(deps.get_db),
) -> schemas.QuizUpdate:
    return await quiz_service.create_quiz(quiz_in, db)


@router.patch(
    "/{quiz_id}",
    response_model=schemas.QuizRead,
    description="응시중인 사용자의 시험지에는 반영되지 않습니다.",
)
async def update_quiz(
    quiz_id: int,
    task_in: schemas.QuizBase,
    _: models.User = Depends(deps.get_current_active_superuser),
    db: AsyncSession = Depends(deps.get_db),
) -> schemas.QuizRead:
    return await quiz_service.update_quiz(quiz_id, task_in, db)


@router.patch(
    "/{question_id}/question",
    response_model=schemas.QuestionUpdate,
    description="응시중인 사용자의 시험지에는 반영되지 않습니다.",
)
async def update_question(
    question_id: int,
    task_in: schemas.QuestionUpdate,
    _: models.User = Depends(deps.get_current_active_superuser),
    db: AsyncSession = Depends(deps.get_db),
) -> schemas.QuestionUpdate:
    return await question_service.update_questions(task_in, db)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: int,
    _: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> None:
    return await quiz_service.delete_quiz(quiz_id, db)


@router.get(
    "/{quiz_id}/detail",
    response_model=schemas.QuizUpdate,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def get_quiz_detail(
    quiz_id: int,
    page: int = 1,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
    redis_client: Redis = Depends(deps.get_redis_client),
) -> schemas.QuizUpdate:
    if crud.user.is_superuser(current_user):
        return await quiz_service.get_questions_by_quiz_id(
            quiz_id=quiz_id,
            current_user=current_user,
            db=db,
            page=page,
            redis_client=redis_client,
        )
    else:
        return await quiz_service.get_questions_by_quiz_id(
            quiz_id=quiz_id,
            current_user=current_user,
            db=db,
            page=page,
            redis_client=redis_client,
        )


@router.get(
    "/{quiz_id}/apply",
    response_model=schemas.QuizRead,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def apply_quiz(
    quiz_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
    redis_client: Redis = Depends(deps.get_redis_client),
) -> schemas.QuizRead:
    return await quiz_service.apply_quiz(
        quiz_id=quiz_id, current_user=current_user, db=db, redis_client=redis_client
    )


@router.post(
    "/{quiz_id}/select",
    status_code=status.HTTP_200_OK,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def select_question_choice(
    quiz_id: int,
    question_idx: int,
    choice: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    redis_client: Redis = Depends(deps.get_redis_client),
):
    return quiz_service.select_question_choice(
        quiz_id=quiz_id,
        question_idx=question_idx,
        choice=choice,
        current_user=current_user,
        redis_client=redis_client,
    )


@router.post(
    "/{quiz_id}/submit",
    response_model=schemas.QuizSubmit,
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def submit_quiz(
    quiz_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    redis_client: Redis = Depends(deps.get_redis_client),
) -> schemas.QuizSubmit:
    return quiz_service.submit_quiz(quiz_id, current_user, redis_client)


@router.get(
    "",
    response_model=list[schemas.QuizRead],
    description="Get tasks by user_id or keyword. If both are None, return 400.",
)
async def get_quiz_handler(
    page: int = 1,
    per_page: int = 10,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> list[schemas.QuizRead]:
    skip: int = (page - 1) * per_page

    if crud.user.is_superuser(user=current_user):
        quiz = await crud.quiz.get_list(db=db, skip=skip, limit=per_page)
    else:
        quiz = await crud.quiz.get_list_by_user_id(
            db=db, user_id=current_user.id, skip=skip, limit=per_page
        )

    logger.debug(quiz)
    return [
        schemas.QuizRead(id=q.id, name=q.name, limit=q.limit, status=q.status)
        for q in quiz
    ]
