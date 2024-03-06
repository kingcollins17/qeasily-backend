# Util functions for user routes mostly

from typing import Any, List, Annotated, Tuple
from fastapi import Depends
import aiomysql
from app import get_db
from app.models.page_request import PageInfo
from app.v_models import *
from app.models.categories_models import Category
from app.db.database import Database


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
