from app import get_db
from typing import List, Any, Annotated

import aiomysql
from fastapi import FastAPI, Depends, HTTPException, Request, status, Request
from app.dependencies.path_deps import get_current_user
from app.models.user_model import User
from app.routes.auth import route as auth_route

from app import SECRET_KEY, PUBLIC_KEY

# from app.routes.admin import route as admin_route
from app.routes.categories_route import cats_router
from app.routes.topic_route import topic_router
from app.routes.follows_route import follow_router
from app.routes.quiz_route import quiz_router
from app.routes.challenge import router as ch_router
from app.routes.questions import router as question_router
from app.routes.activity import activity
from app.routes.transaction import transaction

# from app.utils.security import SECRET
from app.v_models import *
from app.models.plan import plans
from app.utils.util_routes import *
from app.utils.csv_parser import *

# from app.db.database import Database


app = FastAPI(title="Quiz Application Backend")

app.include_router(auth_route, prefix="/auth")
app.include_router(cats_router, prefix="/categories")
app.include_router(topic_router, prefix="/topics")
app.include_router(follow_router, prefix="/follow")
app.include_router(quiz_router, prefix="/quiz")
app.include_router(ch_router, prefix="/challenge")

app.include_router(question_router, prefix="/questions")
app.include_router(activity, prefix="/activity")
app.include_router(transaction, prefix="/transaction")


@app.get("/plans")
async def fetch_plans(user: Annotated[User, Depends(get_current_user)]):
    return {"detail": "Fectched Plans", "data": plans, "user": user}


@app.get("/keys")
async def keys(user: Annotated[User, Depends(get_current_user)]):
    return {"detail": "Successful", "secret_key": SECRET_KEY, "public_key": PUBLIC_KEY}


@app.get("/search")
async def search_resource(
    query: str, db: Annotated[aiomysql.Connection, Depends(get_db)], page: PageInfo
):
    try:
        data = await _search(connection=db, term=query, page=page)
        return {
            "detail": "Found results for " + query,
            "data": {"quiz": data[0], "topics": data[1]},
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# --------------------------------------------------------
# - CRUD OPERATIONS
async def _search(*, connection: aiomysql.Connection, term: str, page: PageInfo):
    query00 = f"""SELECT quiz.*, topics.title as topic, users.user_name as creator FROM quiz 
    LEFT JOIN topics ON quiz.topic_id = topics.id
    LEFT JOIN users ON quiz.user_id = users.id
    WHERE quiz.title REGEXP '{term}' OR 
    quiz.description REGEXP '{term}' ORDER BY quiz.date_added DESC 
    LIMIT %s OFFSET %s"""

    query01 = f"""SELECT topics.*, users.user_name as creator, categories.name as category
    FROM topics LEFT JOIN users on topics.user_id = users.id LEFT JOIN categories ON categories.id = topics.category_id
    WHERE topics.title  REGEXP '{term}' OR topics.description
      REGEXP '{term}' ORDER BY topics.date_added DESC LIMIT %s OFFSET %s"""
    queries = [query00, query01]
    tags = ["quizzes", "topics"]
    result = []

    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        count = 0
        for query in queries:
            await cursor.execute(query, args=(page.per_page + 1, offset(page)))
            data = await cursor.fetchall()
            result.append(data)
    return tuple(result)
