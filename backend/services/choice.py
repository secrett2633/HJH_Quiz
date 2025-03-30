from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend import crud, models


class ChoiceService:
    @staticmethod
    async def read_choice(
        choice_id: int,
        db: AsyncSession,
    ) -> models.Choice:
        choice = await crud.choice.get(db, id=choice_id)

        if choice is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Choice not found"
            )

        return choice

    @staticmethod
    async def delete_choice(
        task_id: int,
        db: AsyncSession,
    ) -> None:
        await choice_service.read_choice(task_id, db)
        await crud.choice.delete(db, id=task_id)

        return


choice_service = ChoiceService()
