from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    """Таблица Users"""
    __tablename__ = 'users_task_2'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String(length=50))
    surname = Column(String(length=50))
    birthday = Column(Date)
    email = Column(String(length=100), unique=True, index=True)
    address = Column(String, nullable=True)

    def __str__(self):
        return f'{self.surname} {self.name}'

    def __repr__(self):
        return f'User(id={self.id}, name={self.name}, surname={self.surname})'
