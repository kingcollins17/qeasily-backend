# crud operation on topics table
from datetime import datetime
import aiomysql
from typing import Dict, Tuple, List
from app.models.page_request import PageInfo
from app.models.topic_models import *
from app.db import PageHandler
from app.utils.util_routes import consume_points


class PagedTopicHandler(PageHandler):
    """Handles pagination and filtering for topics"""
    def __init__(self, *, category_id: int | None = None, 
                 use_following: bool = False, user_id: int | None = None) -> None:
        self.category_id = category_id
        self.use_following = use_following
        self.user_id = user_id
    
    async def _fetch_default(self, *, page: PageInfo, connection: aiomysql.Connection):
        query = """SELECT * FROM topics ORDER BY date_added DESC LIMIT %s OFFSET %s"""
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(query, args=(page.per_page + 1, super()._offset(page)))
            return self._parse(await cursor.fetchall(), page)


    async def fetch_page(self, page: PageInfo, *, connection: aiomysql.Connection):
        if self.use_following:
            return await self.__fetch_use_following(page=page, connection=connection)
        elif self.use_following and self.user_id:
            return await self.__fetch_use_category(page=page, connection=connection)
        else:
            return await self._fetch_default(page=page, connection=connection)

    async def __fetch_use_category(self, *, page: PageInfo,
                                    connection: aiomysql.Connection):
        if self.category_id:
            query = """SELECT * FROM topics WHERE category_id = %s 
                        ORDER BY date_added DESC LIMIT %s OFFSET %s"""
            
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor = cursor

                await cursor.execute(query, args=(self.category_id, page.per_page + 1,
                                                   super()._offset(page)))
                
                return self._parse(await cursor.fetchall(), page)
                
            
        return ([], False)

    # def _parse(self, topics: List[Dict[str, Any]] | None, page: PageInfo):
    #             if topics and (len(topics) > page.per_page):
    #                 return ([topics[i] for i in range(len(topics) - 1)],
    #                          len(topics) > page.per_page)
    #             return (topics, False)


    async def __fetch_use_following(self, * , page: PageInfo, connection: aiomysql.Connection):
        if self.use_following and self.user_id:
            query = """SELECT * FROM topics WHERE user_id IN 
            (SELECT followed_id FROM follows WHERE follower_id = %s) ORDER BY date_added DESC
             LIMIT %s OFFSET %s"""
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor = cursor
                await cursor.execute(query, args=(self.user_id, page.per_page + 1,
                                                   super()._offset(page)))
                res = await cursor.fetchall()
                return super()._parse(res, page)
            

    # def __offset(self, page: PageInfo) -> int:
    #     if page.page <= 1:
    #         return 0
    #     else:
    #         return ((page.page - 1) * page.per_page)


### - add a topic to the database
async def db_add_topic(*, connection: aiomysql.Connection, topics: List[Topic], user_id: int):
    length = len(topics)
    values = ""
    for i in range(length):
        values += f"('{topics[i].title}', '{topics[i].description}', {topics[i].category_id}, {user_id}, {topics[i].level})"
        if i < (length - 1):
            values += ","
    query = f"INSERT INTO topics (title, description, category_id, user_id, level) VALUES {values}"
    insert_id: Any
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await consume_points(cursor, 2, user_id) #consume points first
        await cursor.execute(query=query)
        insert_id = cursor.lastrowid

    await connection.commit()
    return insert_id


async def db_delete_topic(*, connection: aiomysql.Connection, topic_id: int, user_id: int):
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await consume_points(cursor, 2, user_id)
        await cursor.execute(f"DELETE FROM topics WHERE id = {topic_id} AND user_id = {user_id}")
    await connection.commit()
