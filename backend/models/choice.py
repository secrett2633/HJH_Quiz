from sqlalchemy import Boolean, Column, Integer, Text, ForeignKey

from backend.models.base import Base


class Choice(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(Text)
    question_id: int = Column(Integer, ForeignKey("question.id"))
    is_answer: bool = Column(Boolean)
