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

router = APIRouter()


# Data Model
class Mcq(BaseModel):
    query: str
    A: str
    B: str
    C: str
    D: str
    explanation: str
    correct: str
    difficulty: str
    topic_id: int


class Dcq(BaseModel):
    query: str
    correct: bool
    explanation: str
    topic_id: int


@router.get("")
async def fetch_questions(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    quiz_id: int,
    page: PageInfo,
):
    try:
        res = await _fetch_quiz_questions(connection=db, qid=quiz_id, page=page)
        return {"detail": "Questions fetched successfully", **res, "page": page}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get("/all-mcq")
async def fetch_all_mcqs(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    topic_id: int,
    page: PageInfo,
):
    try:
        query00 = "SELECT * FROM mcqs WHERE topic_id = %s ORDER BY id DESC LIMIT %s OFFSET %s"
        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(
                query00, args=(topic_id, page.per_page + 1, offset(page))
            )
            res = _parse_list((await cursor.fetchall()), page)
            return {
                "detail": "Fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get("/created-dcq")
async def fetch_created_dcqs(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
    topic_id: int | None = None,
):
    try:
        query00 = f"SELECT * FROM dcqs WHERE user_id = {user.id}"
        if topic_id:
            query00 += f" AND topic_id = {topic_id}"
        query00 += " ORDER BY id DESC LIMIT %s OFFSET %s"
        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(query00, args=(page.per_page + 1, offset(page)))
            res = _parse_list((await cursor.fetchall()), page)
            return {
                "detail": "Fetched created Questions successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get("/all-dcq")
async def fetch_all_dcq(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    topic_id: int,
    page: PageInfo,
):
    try:
        query = (
            "SELECT * FROM dcqs WHERE topic_id = %s ORDER BY id DESC LIMIT %s OFFSET %s"
        )
        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(
                query, args=(topic_id, page.per_page + 1, offset(page))
            )
            res = _parse_list((await cursor.fetchall()), page)
            return {
                "detail": "Fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.post("/create-dcq")
async def create_dcq(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    dcqs: List[Dcq],
):
    try:
        query00 = "INSERT INTO dcqs (query, correct, explanation, topic_id, user_id) VALUES (%s,%s,%s,%s,%s)"
        data = [
            (dcq.query, dcq.correct, dcq.explanation, dcq.topic_id, user.id)
            for dcq in dcqs
        ]
        async with db.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.executemany(query00, args=data)

        await db.commit()
        return {"detail": "Double choice questions created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get("/created-mcq")
async def fetch_created_mcq(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
    topic_id: int | None = None,
):
    try:
        query = f"SELECT * FROM mcqs WHERE user_id = {user.id}"
        if topic_id:
            query += f" AND topic_id = {topic_id}"
        query += " ORDER BY id DESC LIMIT %s OFFSET %s"
        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(query, args=(page.per_page + 1, offset(page)))
            res = _parse_list((await cursor.fetchall()), page)
            return {
                "details": "Your creations fetched",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.delete("/delete-mcq")
async def delete_mcq(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    ids: List[int],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        query = f"DELETE FROM mcqs WHERE id IN {tuple(ids)} AND user_id = %s"
        async with db.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.execute(query, args=(user.id,))
            await db.commit()
            return {"detail": f"Questions {ids} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.delete("/delete-dcq")
async def delete_dcq(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    ids: List[int],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        query = f"DELETE FROM dcqs WHERE id IN {tuple(ids)} AND user_id = %s"
        async with db.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.execute(query, args=(user.id,))
            await db.commit()
            return {"detail": f"Questions {ids} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.post("/create-mcq")
async def create_questions(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    mcqs: List[Mcq],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        q0 = """INSERT INTO mcqs (query, A, B, C, D, explanation, correct,
      difficulty, topic_id, user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)"""
        data = [
            (
                mcq.query,
                mcq.A,
                mcq.B,
                mcq.C,
                mcq.D,
                mcq.explanation,
                mcq.correct,
                mcq.difficulty,
                mcq.topic_id,
                user.id,
            )
            for mcq in mcqs
        ]
        async with db.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.executemany(q0, args=data)
        await db.commit()
        return {"detail": "Questions added successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# CRUD and UTILITY FUNCTIONS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=


async def _fetch_quiz_questions(
    *, connection: aiomysql.Connection, qid: int, page: PageInfo
):
    #     query00 = "SELECT * FROM mcqs WHERE id in"
    query00 = f"SELECT questions, type FROM quiz WHERE id = {qid}"

    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query00)
        res = await cursor.fetchone()
        _type = res["type"]
        questions = [
            int(value)
            for value in str(res["questions"])
            .removeprefix("[")
            .removesuffix("]")
            .split(",")
        ]
        # return questions, _type
        if _type == "mcq":
            query01 = (
                f"SELECT * FROM mcqs WHERE id IN {tuple(questions)} LIMIT %s OFFSET %s"
            )
        else:
            query01 = (
                f"SELECT * FROM dcqs WHERE id IN {tuple(questions)} LIMIT %s OFFSET %s"
            )

        await cursor.execute(query01, args=(page.per_page + 1, offset(page)))

        res = _parse_list(await cursor.fetchall(), page)
        return {"data": res[0], "has_next_page": res[1]}


def _parse_list(res: List[Any], page: PageInfo) -> Tuple[list[Any], bool]:
    if res and (len(res) > page.per_page):
        return (
            [res[i] for i in range(len(res) - 1)],
            len(res) > page.per_page,
        )
    return (res, False)
