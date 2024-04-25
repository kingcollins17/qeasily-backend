# Writing global and large scoped dependencies here ...
from dotenv import load_dotenv
import os

load_dotenv()


import aiomysql

DB_HOST = str(os.getenv("HOST_DB"))
DB_PORT = int(str(os.getenv("PORT_DB")))
DB_USER = str(os.getenv("USER_DB"))
DB_PASSWORD = str(os.getenv("PASSWORD_DB"))
DB_NAME = str(os.getenv("NAME_DB"))

PUBLIC_KEY = str(os.getenv("P_KEY"))
SECRET_KEY = str(os.getenv("S_KEY"))


credentials: dict = {
    "host": DB_HOST,
    "port": DB_PORT,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "db": DB_NAME,
}
# credentials: dict = {
#     "host": "localhost",
#     "port": 3306,
#     "user": "root",
#     "password": "mysqlking@02",
#     "db": "quiz",
# }


async def get_db():
    db: aiomysql.Connection
    try:
          db = await aiomysql.connect(**credentials) #type: ignore
          yield db
    finally:
          db.close() #type: ignore
