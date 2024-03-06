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


@router.get("")
async def fetch_questions(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    qid: int,
    page: PageInfo,
):
    try:
        res = await _fetch_quiz_questions(connection=db, qid=qid, page=page)
        return {"detail": "Questions fetched successfully", **res, 'page': page}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# CRUD OPERATIONS
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
        return {'data': res[0], 'has_next_page': res[1]}


def _parse_list(res: List[Any], page: PageInfo) -> Tuple[list[Any], bool]:
    if res and (len(res) > page.per_page):
        return (
            [res[i] for i in range(len(res) - 1)],
            len(res) > page.per_page,
        )
    return (res, False)
