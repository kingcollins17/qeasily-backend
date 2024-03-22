from app import get_db

from typing import List, Any, Annotated

import aiomysql
from fastapi import FastAPI, Depends, HTTPException, Request, status, Request
from app.routes.auth import route as auth_route

# from app.routes.admin import route as admin_route
from app.routes.categories_route import cats_router
from app.routes.topic_route import topic_router
from app.routes.follows_route import follow_router
from app.routes.quiz_route import quiz_router
from app.routes.challenge import router as ch_router
from app.routes.questions import router as question_router
from app.routes.activity import activity

from app.v_models import *
from app.utils.util_routes import *
from app.utils.csv_parser import *
from app.db.database import Database


app = FastAPI(title="Quiz Application Backend", docs_url="/swagger")

app.include_router(auth_route, prefix="/auth")
app.include_router(cats_router, prefix="/categories")
app.include_router(topic_router, prefix="/topics")
app.include_router(follow_router, prefix="/follow")
app.include_router(quiz_router, prefix="/quiz")
app.include_router(ch_router, prefix="/challenge")

app.include_router(question_router, prefix="/questions")
app.include_router(activity, prefix="/activity")


@app.get("/search")
async def search_resource(
    query: str, db: Annotated[aiomysql.Connection, Depends(get_db)], page: PageInfo
):
    try:        
          data= await _search(connection=db, term=query, page=page)
          return {'detail': 'Searched ' + query, 'data': data}
    except Exception as e:
          raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# - CRUD OPERATIONS
async def _search(*, connection: aiomysql.Connection, term: str, page: PageInfo):
    query00 = f"""SELECT * FROM quiz WHERE title REGEXP '{term}' OR 
    description REGEXP '{term}' ORDER BY date_added DESC 
    LIMIT %s OFFSET %s"""

    query01 = f"""SELECT * FROM topics WHERE title  REGEXP '{term}' OR description
      REGEXP '{term}' ORDER BY date_added DESC LIMIT %s OFFSET %s"""

    query02 = f"""SELECT * FROM challenges WHERE name REGEXP '{term}' ORDER BY date_added DESC LIMIT %s OFFSET %s"""
    queries = [query00, query01, query02]
    tags = ['quizzes', 'topics', 'challenges']
    result = {}

    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        count=0
        for query in queries:
            await cursor.execute(query, args=(page.per_page + 1, offset(page)))
            data = parse_list(await cursor.fetchall(), page)
            parsed = ({'data': data[0], 'has_next_page': data[1]})
            result = {**result, f'{tags[count]}': parsed}
            count += 1

    return result
