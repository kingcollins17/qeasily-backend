from typing import Any
from datetime import datetime
import abc
import aiomysql



class FollowingCRUD(abc.ABC):
    """Encapsulates functionality for the follows table in db"""
    
    @staticmethod
    async def follow(*, connection: aiomysql.Connection, followed_id: int, follower_id: int):
        if (followed_id != follower_id):
            query = "INSERT INTO follows (follower_id, followed_id) VALUES (%s,%s)"
            async with connection.cursor() as cursor:
                cursor: aiomysql.Cursor = cursor
                await cursor.execute(query, args=(follower_id, followed_id))
            await connection.commit()

    @staticmethod
    async def unfollow(*, connection: aiomysql.Connection, follower_id: int, followed_id: int):
        if(followed_id != follower_id):
            query = "DELETE FROM follows WHERE follower_id = %s AND followed_id = %s"

            async with connection.cursor() as cursor:
                cursor: aiomysql.Cursor = cursor
                await cursor.execute(query, args=(follower_id, followed_id)) 

            await connection.commit()

    @staticmethod
    async def fetch_followers(*, connection: aiomysql.Connection, user_id: int, limit: int = 10, 
                              start_date: datetime = datetime.now()):
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            query = """SELECT * from followings WHERE followed_id = %s AND date_followed < %s
                         ORDER BY date_followed DESC LIMIT %s"""
            await cursor.execute(query, args=(user_id, start_date, limit))
            return await cursor.fetchall()
