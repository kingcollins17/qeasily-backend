#Util functions for user routes mostly

from typing import Any, List, Annotated
from fastapi import Depends
import aiomysql
from app import get_db
from app.models import *
from app.db.database import Database


async def add_quiz_data(*, quiz: List[Quiz], db: aiomysql.Connection):
    for q in quiz:
        q.quiz_data = await Database.fetch_questions(connection=db, ids=q.questions)
    return quiz
    

async def search_item(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    cat: str | None = None,
    topic: str | None = None,
    quiz: str | None = None,
):
    if cat:
        data = await Database.search_category(connection=db, term=cat)
        if data:
            return [
                Category(
                    id=category.id,
                    name=category.name,
                    topics=await Database.fetch_topics(
                        connection=db, category_id=category.id, limit=100
                    ),
                )
                for category in data
                if category.id
            ]
    elif topic:
        return await Database.search_topic(connection=db, search_term=topic)
    elif quiz:
        q=  await Database.fetch_quiz(connection=db, term=quiz)
        return await add_quiz_data(quiz=q, db=db)

