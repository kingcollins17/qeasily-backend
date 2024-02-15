from typing import Any, Dict
import aiomysql
from app.models.user_model import *
from app.utils.security import hash_password


### - 
async def db_create_user(*, connection: aiomysql.Connection, user: RegisterUser):
    user.password = hash_password(user.password)
    query = 'INSERT INTO users (user_name, email, password, type) VALUE (%s,%s,%s,%s)'
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query=query, args=(user.user_name, user.email,
                                                 user.password, user.type))
     
    await connection.commit()
    

### - 
async def db_find_user(*, connection: aiomysql.Connection, email: str) -> Dict[str, Any] | None:
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute("SELECT * FROM users WHERE email = %s", args=(email,))
        return await cursor.fetchone()
        


### - 
async def db_fetch_user_profile(*, connection: aiomysql.Connection, user_id: int) -> Dict[str, Any] | None:
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute("SELECT * FROM users_profile WHERE user_id = %s", args=(user_id,))
        user = await cursor.fetchone()
        return user



### - 
async def db_create_user_profile(*, connection: aiomysql.Connection, profile: UserProfile):
    query = 'INSERT INTO users_profile (first_name, last_name, reg_no, department, level, user_id) VALUES (%s, %s, %s, %s, %s,%s)'
    async with connection.cursor() as cursor:
        
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query=query, args=(profile.first_name, profile.last_name, profile.reg_no,
                                                 profile.department, profile.level, profile.user_id))
    await connection.commit()


### - 
async def db_update_user_profile(*, connection: aiomysql.Connection, profile: UserProfile):
    query = """
            UPDATE users_profile SET first_name = %s, last_name = %s, reg_no = %s,
              department = %s, level = %s WHERE user_id = %s
        """
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query=query, args = (profile.first_name, profile.last_name, 
                                                  profile.reg_no, profile.department, 
                                                  profile.level, profile.user_id))
        
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