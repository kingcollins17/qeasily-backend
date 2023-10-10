from app import get_db

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

@app.get("/topics")
async def get_topics(db: Annotated[aiomysql.Connection, Depends(get_db)], cat: int):
    return await  Database.fetch_topics(connection=db, category_id=cat, limit=1000)
    

@app.get("/categories")
async def get_categories(db: Annotated[aiomysql.Connection, Depends(get_db)]):
    return await Database.fetch_categories(connection=db, limit = 1000)


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
    # a search term
    q: str | None = None,
    topic: int | None = None,
    id: int | None = None,
):
    quiz: List[Quiz] = []
    if q:
        quiz = await Database.fetch_quiz(connection=db, term=q)
    elif topic:
        quiz = await Database.fetch_quiz(connection=db, topic_id=topic)
    elif id:
        quiz = await Database.fetch_quiz(connection=db, id=id)
    else:
        quiz = await Database.fetch_quiz(connection=db)
    # Else, return quiz without quiz data
    return quiz


@app.get("/questions")
async def get_questions(db: Annotated[aiomysql.Connection, Depends(get_db)], quiz: int):
    db_quiz = await Database.fetch_quiz(connection=db, id=quiz)
    if db_quiz:
        questions: List[Question] = await Database.fetch_questions(
            connection=db, ids=db_quiz[0].questions
        )

        return questions
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz object not found")


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
