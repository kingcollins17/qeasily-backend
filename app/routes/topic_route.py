from fastapi import APIRouter, Depends, HTTPException, status
import aiomysql
import pymysql
from datetime import datetime
from typing import Annotated
from app import get_db
from app.dependencies.path_deps import get_current_user
from app.db.topics_crud import *
from app.models.user_model import User
from app.utils.util_routes import *


topic_router = APIRouter()


@topic_router.get("")
async def fetch_topics(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    page: PageInfo,
    user: Annotated[User, Depends(get_current_user)],
    category_id: int | None = None,
    level: str | None = None,
):
    try:
        res = await _fetch_topics(
            connection=db, page=page, category_id=category_id, level=level
        )
        if res:
            return {
                "detail": "Fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }  # type: ignore
        raise Exception("No results")
        # return res
    except pymysql.err.OperationalError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to fetch topics: {err}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to fetch topics: {type(e)}",
        )


@topic_router.get("/created-topics")
async def fetch_user_created_topics(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:
        query = """SELECT topics.*, categories.name as category,
        users.user_name as creator FROM topics    
        LEFT JOIN users ON users.id = topics.user_id 
        LEFT JOIN categories ON topics.category_id = categories.id 
        WHERE topics.user_id = %s 
        ORDER BY date_added DESC LIMIT %s OFFSET %s"""
        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(query, args=(user.id, page.per_page + 1, offset(page)))
            data = parse_list(await cursor.fetchall(), page)
            return {
                "detail": "Fetched successfully",
                "data": data[0],
                "has_next_page": data[1],
                "page": page,
            }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@topic_router.post("/create")
async def add_topic(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    topics: List[Topic],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        insert_id = await db_add_topic(connection=db, topics=topics, user_id=user.id)  # type: ignore
        return {"detail": "Topics added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{e}",
        )


@topic_router.delete("/remove")
async def remove_topic(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    topic: int,
):
    try:
        await db_delete_topic(
            connection=db, topic_id=topic, user_id=user.id  # type: ignore
        )
        # await consume_points(db, 1, user.id) #type: ignore
        return {"detail": "Topic successfully deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to delete topic: {type(e)}",
        )


# -------------------------------------------------------------------------
# HELPER CRUD Functions
# ------------------------------------------------------------------------
async def _fetch_topics(
    *,
    connection: aiomysql.Connection,
    page: PageInfo,
    category_id: int | None = None,
    level: str | None = None,
):
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        query00 = """SELECT topics.*, users.user_name as creator, categories.name as category FROM topics
            LEFT JOIN users on users.id = topics.user_id
            LEFT JOIN categories ON topics.category_id = categories.id {condition} 
            ORDER BY date_added DESC LIMIT %s OFFSET %s"""
        final_query = ""
        if category_id:
            if level:
                final_query = query00.format(
                    condition=f"WHERE topics.category_id = {category_id} AND topics.level REGEXP '{level}'"
                )
            else:
                final_query = query00.format(
                    condition=f"WHERE topics.category_id = {category_id}"
                )
        else:
            final_query = query00.format(condition=" ")

        await cursor.execute(final_query, args=(page.per_page + 1, offset(page)))
        return parse_list(await cursor.fetchall(), page)
