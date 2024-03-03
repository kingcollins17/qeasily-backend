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
    """Fetch quizzes related to a topic"""
    try:
        res = await PagedQuizHandler(topic_id=topic).fetch_page(
            page=page, connection=db
        )
        if res:
            return {
                "detail": "Fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
        raise Exception("No result")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(type(e))
        )


@quiz_router.get("/by-category")
async def fetch_from_category(
    cid: int,
    page: PageInfo,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    level: str | None = None,
):
    """Fetch quizzes based on a broad categoriy"""
    try:
        res = await PagedQuizHandler(category_id=cid, level=level).fetch_page(
            page=page, connection=db
        )
        if res:
            return {
                "detail": "Fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
        raise Exception("No results")
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
        res = await PagedQuizHandler(use_following=True, user_id=user.id).fetch_page(
            page=page, connection=db
        )
        if res:
            return {
                "detail": "Fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
        raise Exception("No results")

    except Exception as e:
        raise HTTPException(
            detail=str(type(e)), status_code=status.HTTP_400_BAD_REQUEST
        )


@quiz_router.delete("/delete")
async def delete_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    qid: int,
):
    try:
        async with db.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.execute(
                f"DELETE FROM quiz WHERE id = {qid} AND user_id = {user.id}"
            )
        await db.commit()
        return {"detail": "Quiz deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# CRUD HELPER FUNCTIONS FOR QUIZ ROUTE
# -----------------------------------------------------------------------------
