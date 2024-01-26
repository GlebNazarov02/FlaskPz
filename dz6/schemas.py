from enum import Enum

from pydantic import BaseModel, Field

class StatusOrder(Enum):
    DONE = 'Выполнена'
    IN_PROGRESS = 'Выполняется'
    CANCELED = 'Отменен'

class UserInSchema(BaseModel):
    name: str
    surname: str
    email: str = Field(max_length=128)
    password: str = Field(min_length=6)

class UserSchema(UserInSchema):
    id: int

class OrderInShema(BaseModel):
    status: StatusOrder
    user_id: int
    goods_id: int
    order_date: str


class OrderSchema(OrderInShema):
    id: int

class GoodsInSchema(BaseModel):
    name: str
    description: str = Field(max_length=256)
    price: int


class GoodsSchema(GoodsInSchema):
    id: int 