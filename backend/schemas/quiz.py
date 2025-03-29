from enum import Enum

from pydantic import BaseModel, Field


class StatusChoices(str, Enum):
    order = "order"
    random = "random"


class ChoiceBase(BaseModel):
    question_id: int | None = None
    name: str
    is_answer: bool

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    quiz_id: int | None = None
    name: str
    choice: list[ChoiceBase]

    class Config:
        orm_mode = True


class QuizBase(BaseModel):
    name: str | None = None
    limit: int | None = None
    status: StatusChoices | None = None
    question: list[QuestionBase] = Field(
        ...,
        examples=[
            [
                QuestionBase(
                    name="주어진 숫자 중 짝수를 모두 고르세요.",
                    choice=[
                        ChoiceBase(name="2", is_answer=True),
                        ChoiceBase(name="10", is_answer=True),
                        ChoiceBase(name="1", is_answer=False),
                    ],
                ),
                QuestionBase(
                    name="다음 중 계절의 이름으로 옳은 것을 고르세요.",
                    choice=[
                        ChoiceBase(name="여름", is_answer=True),
                        ChoiceBase(name="달", is_answer=False),
                        ChoiceBase(name="바람", is_answer=False),
                    ],
                ),
                QuestionBase(
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

    class Config:
        orm_mode = True


class QuizCreate(BaseModel):
    quizzes: list[QuizBase]

    class Config:
        orm_mode = True


class QuizUpdate(BaseModel):
    quizzes: list[QuizBase]

    class Config:
        orm_mode = True
