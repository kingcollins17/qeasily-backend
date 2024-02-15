import aiomysql

from fastapi import Depends, APIRouter, HTTPException, status

from app import get_db
from app.dependencies.path_deps import *
from app.models.user_model import *
from app.db.quiz_crud import *


quiz_router = APIRouter()


@quiz_router.get("")
async def fetch_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)], page: PageInfo, topic: int
):
    try:
        return await PagedQuizHandler(topic_id=topic).fetch_page(
            page=page, connection=db
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(type(e))
        )


@quiz_router.get("/{category_id}")
async def fetch_from_category(
    category_id: int,
    page: PageInfo,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    level: str | None = None,
):
    try:
        return await PagedQuizHandler(category_id=category_id, level=level).fetch_page(
            page=page, connection=db
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(type(e))
        )


@quiz_router.get("/suggested")
async def get_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:
        return await PagedQuizHandler(use_following=True, user_id=user.id).fetch_page(
            page=page, connection=db
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            detail=str(type(e)), status_code=status.HTTP_400_BAD_REQUEST
        )
