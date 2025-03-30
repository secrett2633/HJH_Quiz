from enum import Enum

from pydantic import BaseModel, Field

from backend.models import Quiz
from backend.schemas.question import QuestionCreate, QuestionUpdate
from backend.schemas.choice import ChoiceBase


class StatusChoices(str, Enum):
    order = "order"
    random = "random"


class QuizBase(BaseModel):
    name: str = ""
    limit: int = 100
    status: StatusChoices = StatusChoices.order

    class Config:
        orm_mode = True


class QuizCreate(QuizBase):
    question: list[QuestionCreate] = Field(
        ...,
        examples=[
            [
                QuestionCreate(
                    name="주어진 숫자 중 짝수를 모두 고르세요.",
                    choice=[
                        ChoiceBase(name="2", is_answer=True),
                        ChoiceBase(name="10", is_answer=True),
                        ChoiceBase(name="1", is_answer=False),
                    ],
                ),
                QuestionCreate(
                    name="다음 중 계절의 이름으로 옳은 것을 고르세요.",
                    choice=[
                        ChoiceBase(name="여름", is_answer=True),
                        ChoiceBase(name="달", is_answer=False),
                        ChoiceBase(name="바람", is_answer=False),
                    ],
                ),
                QuestionCreate(
                    name="대한민국의 수도는 어디인가요?",
                    choice=[
                        ChoiceBase(name="서울", is_answer=True),
                        ChoiceBase(name="부산", is_answer=False),
                        ChoiceBase(name="대구", is_answer=False),
                    ],
                ),
            ]
        ],
    )


class QuizRead(QuizBase):
    id: int

    @classmethod
    def build(cls, quiz: Quiz):
        return cls(
            id=quiz.id,
            name=quiz.name,
            limit=quiz.limit,
            status=quiz.status,
        )


class QuizUpdate(QuizBase):
    id: int
    question: list[QuestionUpdate] = []

    @classmethod
    def build(cls, quiz: Quiz):
        return cls(
            id=quiz.id,
            name=quiz.name,
            limit=quiz.limit,
            status=quiz.status,
            question=[QuestionUpdate.build(question) for question in quiz.question],
        )


class QuizSubmit(BaseModel):
    score: int
