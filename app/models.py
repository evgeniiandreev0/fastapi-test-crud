import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class TaskStatus(str, enum.Enum):
    """
    Enum for task status values.
    """

    PENDING = "IN_PROGRESS"
    IN_PROGRESS = "COMPLETED"
    COMPLETED = "PENDING"


class Task(Base):
    """
    Task database model.
    """

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    priority = Column(Integer, default=1)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")


class User(Base):
    """
    User database model.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))

    tasks = relationship("Task", back_populates="user")
