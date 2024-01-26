from enum import Enum

from pydantic import BaseModel, Field


class Status(Enum):
    """Перечисление статусов задач"""
    DONE = 'Выполнена'
    IN_PROGRESS = 'Выполняется'


class TodoInSchema(BaseModel):
    """Схема задачи без id"""
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(default=None, max_length=250)
    status: Status = Status.IN_PROGRESS


class TodoSchema(TodoInSchema):
    """Схема задачи с id"""
    id: int
