from sqlalchemy import Column, ForeignKey, Table

from backend.models.base import Base

user_quiz = Table(
    "user_quiz",
    Base.metadata,
    Column("user_id", ForeignKey("user.id")),
    Column("quiz_id", ForeignKey("quiz.id")),
)
