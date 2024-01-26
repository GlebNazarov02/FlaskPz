from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException
from sqlalchemy import select, delete, insert, update

from database import startup, shutdown, db
from schemas import OrderInShema,GoodsInSchema,UserInSchema,OrderSchema,UserSchema,GoodsSchema
from models import UserModel,Order,Goods

app = FastAPI(title='Dz6')
app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)

@app.get("/users/", response_model=List[UserSchema])
async def get_all_users() -> List[UserSchema]:
    query = select(UserModel)
    users= await db.fetch_all(query)
    return users

@app.post("/users/", response_model=UserSchema)
async def create_user(user: UserInSchema)-> dict:
    query = insert(UserModel)
    new_user = {"name": user.name, "surname": user.surname, "email": user.email, "password": user.password}
    new_user_id = await db.execute(query, new_user)
    return {**new_user, "id": new_user_id}

@app.get("/users/{user_id}",response_model=UserInSchema)
async def get_user(user_id: int)-> UserInSchema:
    query = select(UserModel).where(UserModel.id == user_id)
    user = await db.fetch_one(query)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserInSchema) -> UserSchema:
    query = select(UserModel).where(UserModel.id == user_id)
    user_ = await db.fetch_one(query)
    if user_:
        updated_user = user.dict(exclude_unset=True)
        query = update(UserModel).where(UserModel.id == user_id).values(updated_user)
        await db.execute(query)
        return await db.fetch_one(select(UserModel).where(UserModel.id == user_id))
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}",response_model=str)
async def delete_user(user_id: int):
    query = select(UserModel).where(UserModel.id == user_id)
    user = await db.fetch_one(query)
    if user:
        query = delete(UserModel).where(UserModel.id == user_id)
        await db.execute(query)
        return f'User {user.name} deleted.'
    raise HTTPException(status_code=404, detail="User not found")

# Запросы для заказов
@app.get("/orders/", response_model=List[OrderSchema])
async def get_all_orders() -> List[OrderSchema]:
    query = select(Order)
    orders = await db.fetch_all(query)
    return orders

@app.post("/orders/", response_model=OrderSchema)
async def create_order(order: OrderInShema) -> dict:
    query = insert(Order)
    new_order = {"user_id": order.user_id, "goods_id": order.goods_id, "date": order.order_date, "status": order.status}
    new_order_id = await db.execute(query, new_order)
    return {**new_order, "id": new_order_id}

@app.get("/orders/{order_id}",response_model=OrderInShema)
async def get_order(order_id: int)-> OrderInShema:
    query = select(Order).where(Order.id == order_id)
    order = await db.fetch_one(query)
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")

@app.put("/orders/{order_id}", response_model=OrderSchema)
async def update_order(order_id: int, order: OrderInShema) -> OrderSchema:
    query = select(Order).where(Order.id == order_id)
    order_ = await db.fetch_one(query)
    if order_:
        updated_order = order.dict(exclude_unset=True)
        query = update(Order).where(Order.id == order_id).values(updated_order)
        await db.execute(query)
        return await db.fetch_one(select(Order).where(Order.id == order_id))
    raise HTTPException(status_code=404, detail="Order not found")

@app.delete("/orders/{order_id}",response_model=str)
async def delete_order(order_id: int):
    query = select(Order).where(Order.id == order_id)
    order = await db.fetch_one(query)
    if order:
        query = delete(Order).where(Order.id == order_id)
        await db.execute(query)
        return f'Order {order.id} deleted.'
    raise HTTPException(status_code=404, detail="Order not found")

# Запросы для товаров
@app.get("/goods/", response_model=List[GoodsSchema])
async def get_all_goods() -> List[GoodsSchema]:
    query = select(Goods)
    goods = await db.fetch_all(query)
    return goods

@app.post("/goods/", response_model= GoodsSchema)
async def create_goods(goods:GoodsInSchema) -> dict:
    query = insert(Goods)
    new_goods = {"name": goods.name, "description": goods.description, "price": goods.price}
    new_goods_id = await db.execute(query, new_goods)
    return {**new_goods, "id": new_goods_id}

@app.get("/goods/{goods_id}", response_model=GoodsInSchema)
async def get_goods(goods_id: int) -> GoodsInSchema:
    query = select(Goods).where(Goods.id == goods_id)
    goods = await db.fetch_one(query)
    if goods:
        return goods
    raise HTTPException(status_code=404, detail="Goods not found")

@app.put("/goods/{goods_id}", response_model=GoodsSchema)
async def update_goods(goods_id: int, goods: GoodsInSchema) -> GoodsSchema:
    query = select(Goods).where(Goods.id == goods_id)
    goods_ = await db.fetch_one(query)
    if goods_:
        updated_goods = goods.dict(exclude_unset=True)
        query = update(Goods).where(Goods.id == goods_id).values(updated_goods)
        await db.execute(query)
        return await db.fetch_one(select(Goods).where(Goods.id == goods_id))
    raise HTTPException(status_code=404, detail="Goods not found")

@app.delete("/goods/{goods_id}", response_model=str)
async def delete_goods(goods_id: int):
    query = select(Goods).where(Goods.id == goods_id)
    goods = await db.fetch_one(query)
    if goods:
        query = delete(Goods).where(Goods.id == goods_id)
        await db.execute(query)
        return f'Goods {goods.name} deleted.'
    raise HTTPException(status_code=404, detail="Goods not found")


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)