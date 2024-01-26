import sqlalchemy
import databases
from sqlalchemy.pool import StaticPool
from models import TodoModel

DATABASE_URL = "sqlite:///task3.db"
db = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()


async def startup():
    await db.connect()
    engine = sqlalchemy.create_engine(DATABASE_URL, echo=True, poolclass=StaticPool,
                                      connect_args={"check_same_thread": False})
    TodoModel.metadata.create_all(engine)


async def shutdown():
    await db.disconnect()


async def get_db_session():
    async with db.transaction():
        yield
