from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
import aiomysql
import pymysql
from typing import Annotated
from app import get_db
from app.dependencies.path_deps import get_current_user
from app.models.user_model import *
from app.db.follows_crud import FollowingCRUD


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
    pass
