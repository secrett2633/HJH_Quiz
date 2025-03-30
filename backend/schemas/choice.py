from pydantic import BaseModel

from backend.models.choice import Choice


class ChoiceBase(BaseModel):
    name: str = ""
    is_answer: bool = False


class ChoiceCreate(BaseModel):
    choice: list[ChoiceBase]

    class Config:
        orm_mode = True


class ChoiceUpdate(ChoiceBase):
    id: int

    @classmethod
    def build(cls, choice: Choice):
        return cls(
            id=choice.id,
            name=choice.name,
            is_answer=choice.is_answer,
        )
