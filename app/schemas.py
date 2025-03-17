from datetime import datetime
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class TaskStatus(str, Enum):
    """
    Enum for task status values.
    """

    PENDING = "в ожидании"
    IN_PROGRESS = "в работе"
    COMPLETED = "завершено"


class TaskBase(BaseModel):
    """
    Base schema for tasks.
    """

    title: Annotated[str, Field(max_length=100)]
    description: str | None = None
    status: TaskStatus = TaskStatus.PENDING
    priority: Annotated[int, Field(gt=0, le=10)] = 1


class TaskCreate(TaskBase):
    """
    Schema for task creation.
    """

    pass


class TaskUpdate(TaskBase):
    """
    Schema for task update.
    """

    title: Annotated[str, Field(max_length=100)] | None = None
    status: TaskStatus | None = None
    priority: Annotated[int, Field(gt=0, le=10)] | None = None


class Task(TaskBase):
    """
    Schema for task response.
    """

    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """
    Base schema for users.
    """

    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for user creation.
    """

    password: Annotated[str, Field(min_length=8, max_length=100)]


class User(UserBase):
    """
    Schema for user response.
    """

    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    Schema for token response.
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data.
    """

    username: str | None = None
