#Writing global and large scoped dependencies here ...
from dotenv import load_dotenv
import os

load_dotenv()


import aiomysql

DB_HOST = str(os.getenv("DB_HOST"))
DB_PORT = int(str(os.getenv("DB_PORT")))
DB_USER = str(os.getenv("DB_USER"))
DB_PASSWORD = str(os.getenv("DB_PASSWORD"))
DB_NAME = str(os.getenv("DB_NAME"))


credentials: dict = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "db": DB_NAME,
}


async def get_db():
    db: aiomysql.Connection
    try:
          db = await aiomysql.connect(**credentials) #type: ignore
          yield db
    finally:
          db.close() #type: ignore
    