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
from app.routes.challenge import router as ch_router
from app.routes.questions import router as question_router

from app.v_models import *
from app.utils.util_routes import *
from app.utils.csv_parser import *
from app.db.database import Database


app = FastAPI(title="Quiz Application Backend", docs_url="/swagger")

app.include_router(auth_route, prefix="/auth")
app.include_router(cats_router, prefix='/categories')
app.include_router(topic_router, prefix='/topics')
app.include_router(follow_router, prefix='/follow')
app.include_router(quiz_router, prefix='/quiz')
app.include_router(ch_router, prefix='/challenge')

app.include_router(question_router, prefix="/questions")
