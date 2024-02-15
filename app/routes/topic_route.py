from fastapi import APIRouter, Depends, HTTPException, status
import aiomysql
import pymysql
from datetime import datetime
from typing import Annotated
from app import get_db
from app.dependencies.path_deps import get_current_user
from app.db.topics_crud import *
from app.models.user_model import User


topic_router = APIRouter()


@topic_router.get("")
async def get_topics(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    page: PageInfo,
    user: Annotated[User, Depends(get_current_user)], following: bool = False,
        category: int | None =None,
):
    """user is the id of the user. To fetch topics, you must provide either a start date, a category_id, or user_id"""
    try:
        res =  await PagedTopicHandler(category_id=category, use_following=following, 
                                       user_id=user.id).fetch_page(page, connection=db)
        return {'meta': page,'topics': res[0], 'has_next_page': res[1]} #type: ignore
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


@topic_router.post("/create")
async def add_topic(
    db: Annotated[aiomysql.Connection, Depends(get_db)], topics: List[Topic]
):
    try:
        insert_id = await db_add_topic(connection=db, topics=topics)
        return {
            "detail": "Topics added successfully",
            "topics": f"{insert_id} - {insert_id + (len(topics) - 1)}",
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to add topics {type(e)}",
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
        return {"detail": "Operation successful"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to delete topic: {type(e)}",
        )
