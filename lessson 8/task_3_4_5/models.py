from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///task_3_4_5/db3.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": True})

Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db3 = SessionLocal()


class UsersBase(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    name = Column(String(80), nullable=False)
    email = Column(String(80), nullable=False)
    password = Column(String(80), nullable=False)
    is_del = Column(Boolean, nullable=False)


class Users(BaseModel):
    user_id: int
    name: Optional[str] = None
    email: str
    password: Optional[str] = None
