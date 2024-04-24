from typing import Any, Dict
import aiomysql
from app.models.user_model import *
from app.utils.security import hash_password


### -
async def db_create_user(*, connection: aiomysql.Connection, user: RegisterUser):
    user.password = hash_password(user.password)
    query00 = "INSERT INTO users (user_name, email, password) VALUE (%s,%s,%s)"
    query01 = "INSERT INTO users_profile (department, level, user_id) VALUES (%s, %s, %s)"
    query02 = "INSERT INTO activity (user_id) VALUES (%s)"
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(
            query=query00, args=(user.user_name, user.email, user.password)
        )

        # return [cursor.lastrowid, user.department, user.level]
        user_id = cursor.lastrowid
        if user_id:     
            await cursor.execute(query01, args=(user.department, user.level, cursor.lastrowid))
            await cursor.execute(query02, args=(user_id,))
        else :
            raise Exception('Unable to create account')

    await connection.commit()


### -
async def db_find_user(
    *, connection: aiomysql.Connection, email: str
) -> Dict[str, Any] | None:
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute("SELECT * FROM users WHERE email = %s", args=(email,))
        return await cursor.fetchone()


### -
async def db_fetch_user_profile(
    *, connection: aiomysql.Connection, user_id: int
) -> Dict[str, Any] | None:
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(
            "SELECT * FROM users_profile WHERE user_id = %s", args=(user_id,)
        )
        user = await cursor.fetchone()
        return user


### -
async def db_update_user_profile(
    *, connection: aiomysql.Connection, profile: UserProfile, user_id: int
):
    query = "UPDATE users_profile SET department = %s, level = %s WHERE user_id = %s "
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(
            query=query, args=(profile.department, profile.level, user_id)
        )

    await connection.commit()


### -
async def db_user_has_profile(*, connection: aiomysql.Connection, id: int):
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(f"SELECT COUNT(*) FROM users_profile WHERE user_id = {id}")
        res = await cursor.fetchone()
        if res[0] == 0:
            return False
        return True
