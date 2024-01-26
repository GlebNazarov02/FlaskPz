from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from schemas import Status

Base = declarative_base()


class TodoModel(Base):
    """Таблица Todo"""
    __tablename__ = 'todos_task_3'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(length=50), unique=True, index=True)
    description = Column(String(length=250), index=True)
    status = Column(Enum(Status), nullable=False)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email})'
