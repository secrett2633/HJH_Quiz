import json

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from redis import Redis

from backend import crud, models, schemas


class QuizService:
    @staticmethod
    async def read_quiz(
        quiz_id: int,
        db: AsyncSession,
    ) -> models.Quiz:
        quiz = await crud.quiz.get(db=db, id=quiz_id)

        if quiz is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found"
            )

        return quiz

    @staticmethod
    async def create_quiz(
        quiz_in: schemas.QuizCreate,
        db: AsyncSession,
    ) -> schemas.QuizUpdate:
        quiz: models.Quiz = await crud.quiz.create(db=db, obj_in=quiz_in)

        for question_base in quiz_in.question:
            question_obj = question_base.dict()
            question_obj["quiz_id"] = quiz.id
            question: models.Question = await crud.question.create(
                db=db, obj_in=question_obj
            )
            quiz.question.append(question)

            for choice_base in question_base.choice:
                choice_obj = choice_base.dict()
                choice_obj["question_id"] = question.id
                choice: models.Choice = await crud.choice.create(
                    db=db, obj_in=choice_obj
                )
                question.choice.append(choice)

        return schemas.QuizUpdate.build(quiz)

    @staticmethod
    async def update_quiz(
        quiz_id: int,
        task_in: schemas.QuizBase,
        db: AsyncSession,
    ) -> schemas.QuizRead:
        quiz = await QuizService.read_quiz(quiz_id, db)
        await crud.quiz.update(db=db, db_obj=quiz, obj_in=task_in)

        return schemas.QuizRead.build(quiz)

    @staticmethod
    async def delete_quiz(
        task_id: int,
        db: AsyncSession,
    ) -> None:
        await QuizService.read_quiz(task_id, db)
        await crud.quiz.delete(db, id=task_id)

        return

    @staticmethod
    def get_questions_by_redis(
        user_id: int, quiz_id: int, redis_client: Redis
    ) -> dict | None:
        key: str = f"user:{user_id},quiz_id:{quiz_id}"
        questions: str | None = redis_client.get(key)
        if questions is None:
            return None

        questions = json.loads(questions)
        logger.debug("Question 캐싱된 내용 반환")
        logger.debug(questions)
        return questions

    @staticmethod
    def set_questions_with_redis(
        quiz: models.Quiz, user_id: int, redis_client: Redis
    ) -> None:
        key: str = f"user:{user_id},quiz_id:{quiz.id}"
        questions = schemas.QuizUpdate.build(quiz)
        redis_client.set(key, json.dumps(questions.dict()))
        redis_client.expire(key, 60 * 60 * 24)  # 1day

    @staticmethod
    async def get_questions_by_quiz_id(
        quiz_id: int,
        current_user: models.User,
        db: AsyncSession,
        redis_client: Redis,
        page: int = 0,
    ) -> schemas.QuizUpdate:
        quiz: models.Quiz = await QuizService.read_quiz(quiz_id, db)

        questions: dict | None = quiz_service.get_questions_by_redis(
            user_id=current_user.id, quiz_id=quiz_id, redis_client=redis_client
        )
        if questions is not None:
            logger.debug(questions)
            return schemas.QuizUpdate(**questions)

        skip: int = (page - 1) * quiz.limit
        questions: list[models.Question] = await crud.question.get_list_by_quiz_id(
            quiz_id=quiz.id, limit=quiz.limit, db=db, skip=skip
        )
        logger.debug(questions)

        return schemas.QuizUpdate.build(quiz)

    @staticmethod
    async def apply_quiz(
        quiz_id: int, db: AsyncSession, current_user: models.User, redis_client: Redis
    ) -> schemas.QuizRead:
        quiz: models.Quiz = await QuizService.read_quiz(quiz_id=quiz_id, db=db)
        current_user.quizzes.append(quiz)
        db.add(current_user)
        await db.commit()

        quiz_service.set_questions_with_redis(quiz, current_user.id, redis_client)
        return schemas.QuizRead.build(quiz)

    @staticmethod
    def submit_quiz(
        quiz_id: int, current_user: models.User, redis_client: Redis
    ) -> schemas.QuizSubmit:
        key: str = f"user:{current_user.id},quiz_id:{quiz_id}"
        quiz: str = redis_client.get(key)
        if quiz is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Expired Quiz"
            )

        quiz: dict = json.loads(quiz)
        score: int = 0
        logger.debug(quiz)

        for idx, question in enumerate(quiz.get("question")):
            key: str = f"user:{current_user.id},quiz_id:{quiz_id},question_id:{idx + 1}"
            logger.debug(key)
            user_choice = redis_client.get(key)
            logger.debug(user_choice)
            if user_choice is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{idx + 1}번 문제를 선택하지 않았습니다.",
                )

            choice = question.get("choice")[int(user_choice) - 1]
            logger.debug(f"{idx + 1} 번 문제에서 {user_choice} 을 골랐습니다.")
            if choice.get("is_answer"):
                score += 1
                logger.debug("정답")
            else:
                logger.debug("오답")

        logger.debug(f"score {score}")
        return schemas.QuizSubmit(score=score)

    @staticmethod
    def select_question_choice(
        current_user: models.User,
        quiz_id: int,
        question_idx: int,
        choice: int,
        redis_client: Redis,
    ) -> None:
        key: str = (
            f"user:{current_user.id},quiz_id:{quiz_id},question_idx:{question_idx}"
        )
        logger.debug(key)
        redis_client.set(key, str(choice))
        redis_client.expire(key, 60 * 60 * 24)  # 1day


quiz_service = QuizService()
