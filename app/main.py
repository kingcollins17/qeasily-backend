from app import get_db

from typing import List, Any, Annotated

import aiomysql
from fastapi import FastAPI, Depends, HTTPException, status
from app.routes.auth import route as auth_route
# from app.routes.admin import route as admin_route
from app.routes.categories_route import cats_router
from app.routes.topic_route import topic_router
from app.routes.follows_route import follow_router
from app.routes.quiz_route import quiz_router

from app.v_models import *
from app.utils.util_routes import *
from app.utils.csv_parser import *
from app.db.database import Database


app = FastAPI(title="Quiz Application Backend")

app.include_router(auth_route, prefix="/auth")
# app.include_router(admin_route, prefix="/admin")
app.include_router(cats_router, prefix='/categories')
app.include_router(topic_router, prefix='/topics')
app.include_router(follow_router, prefix='/follow')
app.include_router(quiz_router, prefix='/quiz')


@app.get("/count")
async def get_count_data(db: Annotated[aiomysql.Connection, Depends(get_db)], id: int):
    data = await Database.fetch_count(connection=db, topic_id=id)
    return {"count": data}

@app.get("/search")
async def search(
    item: Annotated[Union[List[Category] , List[Topic] , None], Depends(search_item)]
):
    if item:
        return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=Error(msg="Item was not found!").msg,
    )



@app.get("/questions")
async def get_questions(db: Annotated[aiomysql.Connection, Depends(get_db)], quiz: int):
    db_quiz = await Database.fetch_quiz(connection=db, id=quiz)
    if db_quiz:
        questions: List[Question] = await Database.fetch_questions(
            connection=db, ids=db_quiz[0].questions
        )

        return questions
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Quiz object not found"
    )


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
