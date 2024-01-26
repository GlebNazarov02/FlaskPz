from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserModel(Base):
    """Таблица Users"""
    __tablename__ = 'users_task_1'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String(length=50), unique=True, index=True)
    email = Column(String(length=50), unique=True, index=True)
    password = Column(String, nullable=False)

    def __str__(self):
        return self.username

    def __repr__(self):
        return f'User(id={self.id}, username={self.username}, email={self.email})'
