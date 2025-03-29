from sqlalchemy.ext.asyncio import AsyncSession

from backend.crud.base import CRUDBase
from backend.models.choice import Choice
from backend.schemas.choice import ChoiceCreate, ChoiceUpdate


class CRUDChoice(CRUDBase[Choice, ChoiceCreate, ChoiceUpdate]):
    async def bulk_create(
        self, db: AsyncSession, *, objs_in: list[Choice]
    ) -> list[Choice]:
        db.add_all(objs_in)
        await db.commit()

        return objs_in


choice = CRUDChoice(Choice)
