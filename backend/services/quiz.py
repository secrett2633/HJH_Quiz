import json

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud, models, schemas
from backend.utils.redis import redis_client


class QuizService:
    @staticmethod
    async def read_quiz(
        task_id: int,
        db: AsyncSession,
    ) -> models.Quiz:
        task = await crud.quiz.get(db, id=task_id)

        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

        return task

    @staticmethod
    async def create_bulk_quiz(
        task_in: schemas.QuizCreate,
        db: AsyncSession,
    ):
        quizzes: list[models.Quiz] = []
        for quiz_base in task_in.quizzes:
            quiz: models.Quiz = await crud.quiz.create(db=db, obj_in=quiz_base)

            for question_base in quiz_base.question:
                question_base.quiz_id = quiz.id
                question: models.Question = await crud.question.create(
                    db=db, obj_in=question_base
                )
                quiz.question.append(question)

                for choice_base in question_base.choice:
                    choice_base.question_id = question.id
                    choice: models.Choice = await crud.choice.create(
                        db=db, obj_in=choice_base
                    )
                    question.choice.append(choice)

            quizzes.append(quiz)
        return schemas.QuizCreate(quizzes=quizzes)

    @staticmethod
    async def update_task(
        task_id: int,
        task_in: schemas.QuizCreate,
        current_user: models.User,
        db: AsyncSession,
    ) -> models.Quiz:
        task = await QuizService.read_quiz(task_id, current_user, db)

        if task.status == "in_progress":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        if hasattr(task_in, "keywords") and task_in.keywords is not None:
            keywords = await crud.quiz.bulk_create(db=db, objs_in=task_in.keywords)
            task.keywords = keywords
            del task_in.keywords

        return await crud.quiz.update(db, db_obj=task, obj_in=task_in)

    @staticmethod
    async def delete_quiz(
        task_id: int,
        db: AsyncSession,
    ) -> None:
        await QuizService.read_quiz(task_id, db)
        await crud.quiz.delete(db, id=task_id)

        return

    @staticmethod
    async def get_questions_by_redis(user_id: int, quiz_id: int) -> dict | None:
        key: str = f"user:{user_id},quiz_id:{quiz_id}"
        questions: str | None = redis_client.get(key)
        if questions is None:
            return None

        questions = json.loads(questions)
        print("Question 캐싱된 내용 반환")
        print(questions)
        return questions

    @staticmethod
    async def set_questions_with_redis(quiz, questions, user_id, quiz_id):
        key: str = f"user:{user_id},quiz_id:{quiz_id}"
        questions = schemas.QuizBase(
            name=quiz.name, limit=quiz.limit, status=quiz.status, question=questions
        )
        redis_client.set(key, json.dumps(questions.dict()))
        redis_client.expire(key, 60 * 60 * 24)  # 1day

    @staticmethod
    async def get_questions_by_quiz_id(
        quiz_id: int,
        current_user: models.User,
        db: AsyncSession,
        page: int = 0,
        per_page: int = 100,
    ):
        quiz: models.Quiz | None = await crud.quiz.get(db=db, id=quiz_id)

        questions = await quiz_service.get_questions_by_redis(
            user_id=current_user.id, quiz_id=quiz_id
        )

        if questions is not None:
            return schemas.QuizBase(**questions)

        questions: list[models.Question] = await crud.question.get_list_by_quiz_id(
            quiz_id=quiz.id, limit=quiz.limit, db=db
        )

        await quiz_service.set_questions_with_redis(
            quiz, questions, current_user.id, quiz_id
        )

        return schemas.QuizBase(
            name=quiz.name, limit=quiz.limit, status=quiz.status, question=questions
        )


quiz_service = QuizService()
