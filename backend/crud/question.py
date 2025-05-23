from collections.abc import Sequence
from typing_extensions import override
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.base import CRUDBase
from backend.models.question import Question
from backend.schemas.question import QuestionCreate, QuestionUpdate


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    @override
    async def create(self, db: AsyncSession, *, obj_in: dict) -> Question:
        obj_in.pop("choice", None)

        question: Question = await super().create(db=db, obj_in=obj_in)

        return question

    async def bulk_create(
        self, db: AsyncSession, *, objs_in: list[Question]
    ) -> list[Question]:
        db.add_all(objs_in)
        await db.commit()

        return objs_in

    async def get_list_by_quiz_id(
        self, db: AsyncSession, *, quiz_id: int, skip: int = 0, limit: int = 100
    ) -> Sequence[Question]:
        result = await db.execute(
            select(Question)
            .filter(Question.quiz_id == quiz_id)
            .offset(skip)
            .limit(limit)
        )
        return result.unique().scalars().all()


question = CRUDQuestion(Question)
