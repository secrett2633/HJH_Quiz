from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import override

from backend.crud.base import CRUDBase
from backend.models.quiz import Quiz
from backend.schemas.quiz import QuizCreate, QuizUpdate


class CRUDQuiz(CRUDBase[Quiz, QuizCreate, QuizUpdate]):
    @override
    async def create(self, db: AsyncSession, *, obj_in: QuizCreate) -> Quiz:
        obj_in_data = obj_in.dict()
        obj_in_data.pop("question", None)

        task = await super().create(db=db, obj_in=obj_in_data)

        return task

    async def bulk_create(self, db: AsyncSession, *, objs_in: list) -> list[Quiz]:
        obj_in_data = [self.model(**obj_in.dict()) for obj_in in objs_in]
        db.add_all(obj_in_data)

        await db.commit()

        return objs_in


quiz = CRUDQuiz(Quiz)
