# Задание №2
# Создать веб-приложение на FastAPI, которое будет предоставлять API для
# работы с базой данных пользователей. Пользователь должен иметь
# следующие поля:
# ○ ID (автоматически генерируется при создании пользователя)
# ○ Имя (строка, не менее 2 символов)
# ○ Фамилия (строка, не менее 2 символов)
# ○ Дата рождения (строка в формате "YYYY-MM-DD")
# ○ Email (строка, валидный email)
# ○ Адрес (строка, не менее 5 символов)
# API должен поддерживать следующие операции:
# ○ Добавление пользователя в базу данных
# ○ Получение списка всех пользователей в базе данных
# ○ Получение пользователя по ID
# ○ Обновление пользователя по ID
# ○ Удаление пользователя по ID
# Приложение должно использовать базу данных SQLite3 для хранения
# пользователей.

from typing import List
from datetime import datetime

from fastapi import FastAPI, HTTPException
from sqlalchemy import select, delete, insert, update

from models import UserModel
from schemas import UserInSchema, UserSchema
from database import startup, shutdown, db

app = FastAPI(title='Seminar_6, Task 2')
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    """Получение списка всех пользователей"""
    query = select(UserModel)
    users = await db.fetch_all(query)
    if users:
        return users
    raise HTTPException(status_code=404, detail="Нет ни одного пользователя")


@app.get('/users/{user_id}', response_model=UserSchema)
async def get_single_user(user_id: int):
    """Получение пользователя по ID"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.post("/users/", response_model=UserSchema)
async def create_new_user(user: UserInSchema) -> dict:
    """Добавление пользователя в базу данных"""
    query = insert(UserModel).values(**user.dict())
    new_user_id = await db.execute(query, user.dict())
    return {**user.dict(), "id": new_user_id}


@app.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    """Обновление пользователя по ID"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        updated_user = user.dict(exclude_unset=True)
        query = update(UserModel).where(UserModel.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.id == user_id))
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.delete("/users/{user_id}", response_model=str)
async def delete_user(user_id: int) -> str:
    """Удаление пользователя по ID"""
    query = select(UserModel).where(UserModel.id == user_id)
    db_user = await db.fetch_one(query)
    if db_user:
        query = delete(UserModel).where(UserModel.id == user_id)
        await db.execute(query)
        return f'Пользователь с id={db_user.id} удален'
    raise HTTPException(status_code=404, detail="Пользователь не найден")


if __name__ == '__main__':
    import asyncio

    asyncio.run(startup())


    async def virgin_db():
        query = delete(UserModel)
        await db.execute(query)
        query = insert(UserModel)

        for i in range(1, 11):
            birthday_str = f'20{10 + i}-01-01'
            birthday_date = datetime.strptime(birthday_str, '%Y-%m-%d').date()
            new_user = {"name": f"name{i}", "email": f"user{i}@mail.ru",
                        "surname": f"user{i}", "birthday": birthday_date,
                        'address': f'address{i}'}
            await db.execute(query, new_user)


    asyncio.run(virgin_db())
