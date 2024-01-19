from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///task2/db2.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": True})

Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, bind=engine)
db2 = SessionLocal()


class MoviesBase(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, nullable=False)
    title = Column(String(80), nullable=False)
    description = Column(String(80), nullable=False)
    genre = Column(String(80), nullable=False)
    is_del = Column(Boolean, nullable=False)


class Movies(BaseModel):
    movie_id: int
    title: Optional[str] = None
    description: str
    genre: Optional[str] = None
