from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from backend.models.base import Base

if TYPE_CHECKING:
    from backend.models.quiz import Quiz


class User(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    username: str = Column(String, unique=True)
    password: str = Column(String)
    phone_number: str = Column(String(20))
    first_name: str = Column(String(30))
    last_name: str = Column(String(30))
    created: datetime = Column(DateTime(timezone=True), server_default=func.now())
    updated: datetime = Column(DateTime(timezone=True), onupdate=func.now())
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)

    quizzes: Mapped[list["Quiz"]] = relationship(secondary="user_quiz", lazy="selectin")
