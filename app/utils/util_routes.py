#Util functions for user routes mostly

from typing import Any, List, Annotated
from fastapi import Depends
import aiomysql
from app import get_db
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