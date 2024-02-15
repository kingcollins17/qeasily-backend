from typing import Any, List, Tuple
import aiomysql
from app.models.page_request import PageInfo
from app.db import PageHandler


class PagedQuizHandler(PageHandler):
    """Handles pagination for quiz data from db"""

    def __init__(
        self,
        use_likes: bool = False,
        use_following: bool = False,
        search_term: str | None = None,
        topic_id: int | None = None,
        level: str | None = None,
        category_id: int | None = None,
        user_id: int | None = None
    ) -> None:
        """The other of preferences for filters is use_following > topic_Id > category_id > level
        > use_likes > search_term"""
        self.use_likes = use_likes
        self.search_term = search_term
        self.topic_id = topic_id
        self.category_id = category_id
        self.level = level 
        self.use_following = use_following

        # If use_following is true, then user_id must be provided
        self.user_id = user_id

        pass

    async def fetch_page(self, *, page: PageInfo, connection: aiomysql.Connection):
        # res: Any | None = None
        if self.use_following and self.user_id:
            return await self._from_suggested(page=page, connection=connection)
        elif self.topic_id:
            return await self._from_topics(page=page, connection=connection)
        elif self.category_id:
            return await self._from_category(page=page, connection=connection)
        pass

    async def _from_suggested(self, *, page: PageInfo, connection: aiomysql.Connection):
        res: List[Any] | None = None
        if self.use_following and self.user_id:
            query = """SELECT * from quiz WHERE user_id IN 
                    (SELECT followed_id FROM follows WHERE follower_id = %s) 
                    ORDER BY date_added DESC LIMIT %s OFFSET %s"""
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor = cursor
                await cursor.execute(
                    query, args=(self.user_id, page.per_page + 1, super()._offset(page))
                )
                res = await cursor.fetchall()

        return super()._parse(res, page)

    async def _from_search_term(
        self, *, page: PageInfo, connection: aiomysql.Connection
    ):
        if self.search_term:
            pass

    async def _from_topics(self, *, page: PageInfo, connection: aiomysql.Connection):
        res: List[Any] | None = None
        if self.topic_id:
            query = """SELECT * FROM quiz WHERE topic_id = %s 
                    ORDER BY date_added DESC LIMIT %s OFFSET %s"""
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor = cursor
                await cursor.execute(
                    query, args=(self.topic_id, page.per_page + 1, super()._offset(page))
                )
                res = await cursor.fetchall()

        return super()._parse(res, page)

    async def _from_category(self,*, page: PageInfo, connection: aiomysql.Connection):
        res: List[Any] | None =None
        if self.category_id:
            query: str = ''
            args: Tuple
            if self.level:
                query = """SELECT * FROM quiz WHERE topic_id IN 
                (SELECT id FROM topics WHERE category_id = %s AND level = %s) 
                ORDER BY date_added DESC LIMIT %s OFFSET %s"""
                args = (self.category_id, self.level, page.per_page + 1, super()._offset(page))
            else:
                query = """SELECT * FROM quiz WHERE topic_id IN 
                (SELECT id FROM topics WHERE category_id = %s) 
                ORDER BY date_added DESC LIMIT %s OFFSET %s"""
        
                args = (self.category_id, page.per_page + 1, super()._offset(page))

            async with connection.cursor(aiomysql.DictCursor) as cursor:
                cursor: aiomysql.DictCursor = cursor
                await cursor.execute(query, args=args)
                res = await cursor.fetchall()
                # print(res)
        
        return super()._parse(res, page)
