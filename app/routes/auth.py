from typing import Annotated, Any, List, Tuple

import aiomysql
import pymysql
from fastapi import APIRouter, Depends, HTTPException, status

from app import get_db
from app.db.database import Database
from app.db.user_crud import *
from app.dependencies.auth_deps import authenticate
from app.dependencies.path_deps import get_current_user
from app.v_models import *
from app.models.user_model import *
from app.utils.security import *

route = APIRouter()


@route.get("/user")
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user


@route.post("/register")
async def register_user(
    user: RegisterUser, db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    try:
        response = await db_create_user(connection=db, user=user)
        return {"detail": f"User {user.email} created successfully", "data": response}

    except pymysql.IntegrityError:
        raise HTTPException(
            detail="User already has an account",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    #
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@route.put("/update-profile")
async def update_profile(
    profile: UserProfile,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):

    try:
        async with db.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.execute(
                "UPDATE users_profile SET department = %s, level = %s WHERE user_id = %s",
                args=(profile.department, profile.level, user.id),
            )
            await db.commit()
            return {"detail": "Profile updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@route.post("/login")
async def login_user(user: Annotated[LoginUser, Depends(authenticate)]):
    return {"token": create_access_token(data=user.model_dump()), "user": user}


@route.get("/dashboard")
async def get_dashboard(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        data = await fetch_dashboard(connection=db, user_id=user.id)  # type: ignore
        return {"detail": "Fetched dashboard successfully", "data": data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# CRUD OPERATIONS
async def fetch_dashboard(*, connection: aiomysql.Connection, user_id: int):

    query00 = "SELECT * FROM users_profile WHERE user_id = %s"
    query01 = "SELECT * FROM activity WHERE user_id = %s"
    query02 = "SELECT * FROM _qstats WHERE id = %s"
    query03 = "SELECT COUNT(*) as total_mcqs FROM mcqs WHERE user_id = %s"
    query04 = "SELECT COUNT(*) as total_dcqs FROM dcqs WHERE user_id = %s"
    query05 = "SELECT COUNT(*) as following FROM follows WHERE follower_id = %s"

    queries = [query00, query01, query02, query03, query04, query05]
    results: List[Any] = []
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        for query in queries:
            await cursor.execute(query, args=(user_id,))
            results.append(await cursor.fetchone())
    result_dict = {}
    for data in results:
        result_dict = {**result_dict, **data}
    return result_dict
