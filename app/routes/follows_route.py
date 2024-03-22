from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
import aiomysql
import pymysql
from typing import Annotated
from app import get_db
from app.dependencies.path_deps import get_current_user
from app.models.page_request import PageInfo
from app.models.user_model import *
from app.db.follows_crud import FollowingCRUD
from app.utils.util_routes import offset, parse_list


follow_router = APIRouter()


@follow_router.post("")
async def follow_user(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    id: int,
):
    """id HERE refers to the id of the account that is being followed"""

    try:
        await FollowingCRUD.follow(connection=db, followed_id=id, follower_id=user.id)  # type: ignore
        return {"detail": "User followed"}
    except pymysql.err.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already followed by you"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to follow user {type(e)}",
        )


@follow_router.delete("")
async def unfollow_user(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    id: int,
):
    """id refers to the id of the user that needs to be unfollowed"""
    await FollowingCRUD.unfollow(
        connection=db, followed_id=id, follower_id=user.id  # type:ignore
    )
    return {"detail": "Unfollowed user"}


@follow_router.get("/followers")
async def get_followers(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:    
        data =  await fetch_followers(connection=db, user_id=user.id, page=page) #type: ignore
        return {'detail': 'Fetched successfully', 'data': data[0], 'has_next_page': data[1]}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@follow_router.get("/accounts")
async def fetch_users(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:
        data = await suggest_accounts(connection=db, user=user, page=page)
        return {"detail": "Fetched accounts", "data": data}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def fetch_followers(
    *, connection: aiomysql.Connection, user_id: int, page: PageInfo
):
    q0 = "SELECT * FROM followings WHERE followed_id = %s ORDER BY date_followed DESC LIMIT %s OFFSET %s"
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(q0, args=(user_id, page.per_page + 1, offset(page)))
        data = await cursor.fetchall()
        return parse_list(data, page)


async def suggest_accounts(
    *, connection: aiomysql.Connection, user: User, page: PageInfo
):
    query00 = f"SELECT department, level FROM users_profile WHERE user_id = {user.id}"
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query00)
        temp = await cursor.fetchone()
        if temp:
            dept = temp["department"]
            level = temp["level"]

            query01 = """SELECT users.id, users.user_name, users_profile.department, 
             users_profile.level, _qstats.type, _qstats.followers, _qstats.topics, _qstats.total_quiz 
             FROM users RIGHT JOIN users_profile ON
             users.id = users_profile.user_id LEFT JOIN _qstats ON users.id = _qstats.id 
             WHERE users_profile.department REGEXP %s AND users.id != %s AND users.type = 'Admin' 
             ORDER BY _qstats.total_quiz DESC LIMIT %s OFFSET %s"""
            # NOTE Complete function
            await cursor.execute(
                query01, args=(dept, user.id, page.per_page + 1, offset(page))
            )
            return await cursor.fetchall()

        raise Exception("User does not have any profile data")
