import datetime

from pydantic import EmailStr, BaseModel, Field


class UserInSchema(BaseModel):
    """Модель пользователя без id"""
    name: str = Field(..., min_length=2,
                      title='Задается имя пользователя')
    surname: str = Field(..., min_length=2,
                         title='Задается фамилия пользователя')
    birthday: datetime.date = Field(..., title='Задается день рождения пользователя в формате "YYYY-MM-DD"')
    email: EmailStr = Field(..., title='Задается email пользователя')
    address: str = Field(default=None, min_length=5, title='Задается адрес пользователя')


class UserSchema(UserInSchema):
    """Модель пользователя с id"""
    id: int
