from app import get_db
from dotenv import load_dotenv

from typing import List, Any, Annotated

import aiomysql
from fastapi import FastAPI, Depends, HTTPException, status
from app.routes.auth import route as auth_route
from app.routes.admin import route as admin_route

from app.models import *
from app.utils.util_routes import *
from app.utils.util_functions import *
from app.db.database import Database


app = FastAPI(title="Quiz Application Backend")

app.include_router(auth_route, prefix="/auth")
app.include_router(admin_route, prefix="/admin")


@app.get("/")
async def index(db: Annotated[aiomysql.Connection, Depends(get_db)]) -> List[Category]:
    data = await Database.fetch_categories(connection=db)
    categories = [
        Category(
            id=cat.id,
            name=cat.name,
            topics=await Database.fetch_topics(
                connection=db, category_id=cat.id, limit=10
            ),
        )
        for cat in data
        if cat.id
    ]
    return categories


@app.get("/search")
async def search(
    item: Annotated[List[Category] | List[Topic] | None, Depends(search_item)]
):
    if item:
        return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=Error(msg="Item was not found!").msg,
    )


@app.get("/quiz")
async def get_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    # Whether quiz should be accompanied with actual question data
    data: int = 0,
    # a search term
    q: str | None = None,
    topic: int | None = None,
):
    quiz: List[Quiz] = []
    if q:
        quiz = await Database.fetch_quiz(connection=db, term=q)
    elif topic:
        quiz = await Database.fetch_quiz(connection=db, topic_id=topic)
    else:
        quiz = await Database.fetch_quiz(connection=db)
    if data == 1:
        return await add_quiz_data(db=db, quiz=quiz)
    # Else, return quiz without quiz data
    return quiz


@app.get("/quiz/quickstart")
async def quick_start(
    db: Annotated[aiomysql.Connection, Depends(get_db)], conf: QuickStartConf
):
    questions = await Database.fetch_questions(
        connection=db, topics=conf.topics, limit=conf.total_questions * 2
    )
    selected = select_random(
        conf.total_questions, integers=[q.id for q in questions if q.id]
    )

    return [question for question in questions if question.id in selected]

    pass
