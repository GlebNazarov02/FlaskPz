from pydantic import BaseModel, Field
from schemas import StatusOrder
from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'
    id: int  = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name:str = Column(String(length=50), index=True)
    surname:str = Column(String(length=50), index=True)
    email:str = Column(String(length=50), unique=True, index=True)
    password:str = Column(String(length=50), unique=True, index=True)
    

class Order(Base):
    __tablename__ = 'orders'
    id: int  = Column(Integer, autoincrement=True, primary_key=True, index=True)
    user_id: int  = Column(Integer, index=True)
    goods_id: int  = Column(Integer, index=True)
    order_date:str =  Column(String(length=50), index=True)
    status:StatusOrder = Column(Enum(StatusOrder), nullable=False)



class Goods(Base):
    __tablename__ = 'goods'
    id: int   = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name:str = Column(String(length=50), unique=True, index=True)
    description:str = Column(String(length=256), index=True)
    price: int  = Column(Integer, index=True)