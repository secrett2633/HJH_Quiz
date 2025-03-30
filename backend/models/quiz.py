from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import Mapped, relationship

from backend.models.base import Base
from backend.models.user_quiz import user_quiz
from backend.models.question import Question
from backend.models.user import User


class Quiz(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(Text)
    status: str = Column(
        Enum(
            "order",
            "random",
            name="quiz_status",
        ),
        default="order",
    )
    limit: int = Column(Integer)
    question: Mapped[list["Question"]] = relationship("Question", lazy="joined")
    users: Mapped[list["User"]] = relationship(
        "User", secondary=user_quiz, back_populates="quizzes"
    )
