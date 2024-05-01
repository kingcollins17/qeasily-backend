# Util functions for user routes mostly

from typing import Any, List, Annotated, Tuple
from fastapi import Depends
import aiomysql
import pymysql
from app import get_db
from app.models.page_request import PageInfo
from app.v_models import *
from app.models.categories_models import Category
from app.db.database import Database

CREDIT_EXHAUSTED = "You have exhausted your admin credits. Buy an admin package to get more credits"


async def add_quiz_data(*, quiz: List[Quiz], db: aiomysql.Connection):
    for q in quiz:
        q.quiz_data = await Database.fetch_questions(connection=db, ids=q.questions)
    return quiz


async def search_item(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    cat: Union[str, None] = None,
    topic: Union[str, None] = None,
    quiz: Union[str, None] = None,
):
    pass


def offset(page: PageInfo) -> int:
    if page.page <= 1:
        return 0
    else:
        return (page.page - 1) * page.per_page


def parse_list(res: List[Any], page: PageInfo) -> Tuple[list[Any], bool]:
    if res and (len(res) > page.per_page):
        return (
            [res[i] for i in range(len(res) - 1)],
            len(res) > page.per_page,
        )
    return (res, False)


async def consume_points(cursor: aiomysql.Cursor, points: int, user_id: int):
    await cursor.execute('SELECT admin_points FROM activity WHERE user_id = %s', args=(user_id,))
    currentpoints = (await cursor.fetchone())[0]
    if (currentpoints < 1): raise Exception(CREDIT_EXHAUSTED)
    query = "UPDATE activity SET admin_points = admin_points - %s WHERE user_id = %s"
    await cursor.execute(query, args=(points, user_id))
