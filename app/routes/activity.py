from typing import Annotated, Any, List, Tuple

import aiomysql
import pymysql
from fastapi import APIRouter, Depends, HTTPException, status

from app import get_db
from app.db.database import Database
from app.models.page_request import PageInfo
from app.db.user_crud import *
from app.dependencies.auth_deps import authenticate
from app.dependencies.path_deps import get_current_user
from app.v_models import *
from app.models.user_model import *
from app.utils.security import *
from app.utils.util_routes import offset


activity = APIRouter()


@activity.get("")
async def fetch_activity(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        data = res = await check_activity(connection=db, user_id=user.id)  # type: ignore
        return {"detail": "Fetched activity successfully", "data": res}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# @activity.get("/consume-challenge")
# async def complete_challenge(
#     db: Annotated[aiomysql.Connection, Depends(get_db)],
#     user: Annotated[User, Depends(get_current_user)],
# ):

#     try:
#         await consume_challenge(connection=db, user_id=user.id)  # type: ignore
#         return {"detail": "Challenge Consumed successfully"}
#     except pymysql.OperationalError:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="You have reached the limit of your plan, please buy more credits",
#         )
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@activity.get("/consume-quiz")
async def complete_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):

    try:
        res = await consume_quiz(connection=db, user_id=user.id)  # type: ignore
        return {"detail": "Successful, please enjoy your session"}

    except pymysql.OperationalError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have exhausted all available Quiz credits, buy a package to get more credits",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@activity.post("/create")
async def test(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        await create_activity(connection=db, user_id=user.id)  # type: ignore
        return {"detail": "You have set up Account activity"}
    except pymysql.err.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already have an activity",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# CRUD OPERATIONS
async def create_activity(*, connection: aiomysql.Connection, user_id: int):
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(
            "INSERT INTO activity (user_id) VALUES (%s)", args=(user_id,)
        )
    await connection.commit()


async def check_activity(*, connection: aiomysql.Connection, user_id: int):
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute("SELECT * from activity WHERE user_id = %s", args=(5,))
        data = await cursor.fetchone()
        if data:
            return data
        # else
        raise Exception("You do not have any activity!")


async def consume_quiz(*, connection: aiomysql.Connection, user_id: int):
    query = "UPDATE activity SET quizzes_left = quizzes_left - 1 WHERE user_id = %s"
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query, args=(user_id))

    await connection.commit()


# async def consume_challenge(*, connection: aiomysql.Connection, user_id: int):
#     query = (
#         "UPDATE activity SET challenges_left = challenges_left - 1 WHERE user_id = %s"
#     )
#     async with connection.cursor() as cursor:
#         cursor: aiomysql.Cursor = cursor
#         await cursor.execute(query, args=(user_id,))

#     await connection.commit()
