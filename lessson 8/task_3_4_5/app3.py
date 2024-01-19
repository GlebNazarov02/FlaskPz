# Задание №3
# 📌 Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.
# 📌 Создайте модуль приложения и настройте сервер и маршрутизацию.
# 📌 Создайте класс User с полями id, name, email и password.
# 📌 Создайте список users для хранения пользователей.
# 📌 Создайте маршрут для добавления нового пользователя (метод POST).
# 📌 Реализуйте валидацию данных запроса и ответа.

import logging
from fastapi import FastAPI
from task_3_4_5.models import Users, UsersBase, Base, engine, db3

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app3 = FastAPI()


@app3.get("/users/")
async def read_root():
    res = []
    logger.info('Отработал GET запрос.')
    users = db3.query(UsersBase).all()
    for user in users:
        res.append(f"  user_id: {user.user_id},"
                   f" name: {user.name}, email: {user.email}")
    return res


@app3.get("/users/{user_id}")
async def read_root(user_id: int):
    logger.info('Отработал GET запрос.')
    user = db3.query(UsersBase).filter(UsersBase.user_id == user_id).first()
    return f"User: user_id: {user.user_id}, " \
        f"name: {user.name}, email: {user.email}  "


@app3.post("/users/{user_id}")
async def create_item(user_id: int, user: Users):
    logger.info('Отработал POST запрос.')
    users = db3.query(UsersBase).filter(UsersBase.user_id == user_id).all()
    for user in users:
        if user.user_id == user_id:
            return f'Movie already exist!'
    else:
        user = UsersBase(user_id=user.user_id, name=user.name,
                         email=user.email, password=user.password, is_del=False)
        db3.add(user)
        db3.commit()
        return f"User: user_id: {user.user_id}, " \
            f"name: {user.name}, email: {user.email}  "


@app3.put("/users/{user_id}")
async def update_item(user_id: int, user_upd: Users):
    logger.info(f'Отработал PUT запрос для movie id = {user_id}.')
    user = db3.query(UsersBase).filter(UsersBase.user_id == user_id).first()
    user.name = user_upd.name
    user.email = user_upd.email
    user.password = user_upd.password
    db3.commit()
    return {"user_id": user_id, "user": user_upd}


@app3.delete("/users/{user_id}")
async def delete_item(user_id: int):
    logger.info(f'Отработал DELETE запрос для movie id = {user_id}.')
    users = db3.query(UsersBase).filter(UsersBase.user_id == user_id).all()
    for user in users:
        db3.delete(user)
        db3.commit()
    return {"user_id": user_id}
