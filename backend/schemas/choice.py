from enum import Enum

from pydantic import BaseModel


class StatusChoices(str, Enum):
    order = "order"
    random = "random"


class ChoiceBase(BaseModel):
    name: str
    is_answer: bool


class QuestionBase(BaseModel):
    name: str
    choice: list[ChoiceBase]


class QuizBase(BaseModel):
    name: str | None = None
    limit: int | None = None
    status: StatusChoices | None = None
    question: list[QuestionBase]


class ChoiceCreate(BaseModel):
    quizzes: list[QuizBase]

    class Config:
        orm_mode = True


class ChoiceUpdate(BaseModel):
    quizzes: list[QuizBase]

    class Config:
        orm_mode = True
