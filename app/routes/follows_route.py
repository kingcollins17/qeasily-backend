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


@follow_router.get("/followings")
async def get_followings(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:
        data = await fetch_followings(connection=db, user_id=user.id, page=page)  # type: ignore
        return {
            "detail": "Fetch successful",
            "data": data[0],
            "has_next_page": data[1],
            "page": page,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@follow_router.get("/followers")
async def get_followers(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:
        data = await fetch_followers(connection=db, user_id=user.id, page=page)  # type: ignore
        return {
            "detail": "Fetched successfully",
            "data": data[0],
            "has_next_page": data[1],
        }
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
        return {
            "detail": "Fetched accounts",
            "data": data[0],
            "has_next_page": data[1],
            "page": page,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Fetch the accounts that are following your from db
async def fetch_followers(
    *, connection: aiomysql.Connection, user_id: int, page: PageInfo
):
    query00 = """SELECT * FROM profile_data WHERE id in
      (SELECT follower_id FROM follows WHERE followed_id = %s)
      ORDER BY id DESC LIMIT %s OFFSET %s """

    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query00, args=(user_id, page.per_page + 1, offset(page)))
        data = await cursor.fetchall()
        return parse_list(data, page)


# Fetch accounts the user with user_id is following
async def fetch_followings(
    *, connection: aiomysql.Connection, user_id: int, page: PageInfo
):
    """Fetched a list of accounts you are following from the database"""
    query = """SELECT * FROM profile_data WHERE id IN (SELECT followed_id FROM follows WHERE 
    follower_id = %s) ORDER BY id DESC LIMIT %s OFFSET %s"""
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query, args=(user_id, page.per_page + 1, offset(page)))

        return parse_list(await cursor.fetchall(), page)


async def suggest_accounts(
    *, connection: aiomysql.Connection, user: User, page: PageInfo
):
    # query00 = f"SELECT followed_id FROM follows WHERE follower_id = {user.id}"
    query01 = f"SELECT department, level FROM users_profile WHERE user_id = {user.id}"
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query01)
        temp = await cursor.fetchone()
        if temp:
            dept = temp["department"]
            # level = temp["level"]

            query02 = """SELECT * FROM profile_data WHERE department REGEXP '{department}'
            AND (type = 'Admin') AND  id NOT IN (SELECT followed_id FROM follows WHERE follower_id = {user_id}) 
            ORDER BY total_quiz DESC LIMIT %s OFFSET %s"""

            # NOTE Complete function

            await cursor.execute(
                query02.format(user_id=user.id, department=dept),
                args=(page.per_page + 1, offset(page)),
            )
            return parse_list(await cursor.fetchall(), page)

        raise Exception("User does not have any profile data")
