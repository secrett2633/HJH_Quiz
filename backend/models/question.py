from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from backend.models.base import Base
from backend.models.choice import Choice


class Question(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(Text)
    quiz_id: int = Column(Integer, ForeignKey("quiz.id", ondelete="CASCADE"))
    choice: Mapped[list["Choice"]] = relationship("Choice", lazy="joined")
