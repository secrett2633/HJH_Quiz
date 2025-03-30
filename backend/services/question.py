from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud, models, schemas
from backend.services.choice import choice_service


class QuestionService:
    @staticmethod
    async def read_question(
        question_id: int,
        db: AsyncSession,
    ) -> models.question:
        question = await crud.question.get(db=db, id=question_id)

        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
            )

        return question

    @staticmethod
    async def delete_question(
        question_id: int,
        db: AsyncSession,
    ) -> None:
        await question_service.read_question(question_id, db)
        await crud.question.delete(db=db, id=question_id)

        return

    @staticmethod
    def validate_question(question: models.Question) -> None:
        if len(question.choice) < 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Question must have at least 3 choices",
            )

        if not any(c.is_answer for c in question.choice):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one choice must be is_answer",
            )

    @staticmethod
    async def update_questions(
        question_in: schemas.QuestionUpdate,
        db: AsyncSession,
    ) -> models.Quiz:
        for choice_base in question_in.choice:
            choice: models.Choice = await choice_service.read_choice(
                choice_id=choice_base.id, db=db
            )
            await crud.choice.update(
                db=db,
                db_obj=choice,
                obj_in=choice_base,
            )
        question: models.Question = await QuestionService.read_question(
            question_in.id, db
        )
        question_obj = question_in.dict(exclude_unset=True)
        question_obj.pop("choice")
        await crud.question.update(db=db, db_obj=question, obj_in=question_obj)

        question_service.validate_question(question)

        return schemas.QuestionUpdate.build(question)


question_service = QuestionService()
