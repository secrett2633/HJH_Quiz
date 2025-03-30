from pydantic import BaseModel

from backend.schemas.choice import ChoiceBase, ChoiceUpdate
from backend.models.question import Question


class QuestionBase(BaseModel):
    name: str = ""


class QuestionCreate(QuestionBase):
    choice: list[ChoiceBase]


class QuestionUpdate(QuestionBase):
    id: int
    choice: list[ChoiceUpdate]

    @classmethod
    def build(cls, question: Question):
        return cls(
            id=question.id,
            name=question.name,
            choice=[ChoiceUpdate.build(choice) for choice in question.choice],
        )
