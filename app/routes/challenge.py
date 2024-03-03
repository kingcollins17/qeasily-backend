from typing import Annotated, Any, List

import aiomysql
import pymysql
from fastapi import APIRouter, Depends, HTTPException, status

from app import get_db
from app.db.database import Database
from app.db.user_crud import *
from app.dependencies.auth_deps import authenticate
from app.dependencies.path_deps import get_current_user
from app.models.page_request import PageInfo
from app.v_models import *
from app.models.user_model import *
from app.utils.security import *


router = APIRouter()


@router.get("")
async def get_challenges(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
    feed: bool = False,
):
    try:
        res = await _fetch_challenges(connection=db, feed=feed, page=page, id=user.id)
        return {
            "detail": "Fetched successfully",
            "challenges": res[0],
            "has_next_page": res[1],
            "page": page,
        }

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def _fetch_challenges(
    *, connection: aiomysql.Connection, feed: bool, page: PageInfo, id: int | None = None
):
    query = """SELECT * FROM challenges """
    if feed == True and id:
        query += f'WHERE user_id IN (SELECT followed_id FROM follows WHERE follower_id = {id}) '

    query += 'ORDER BY date_added DESC LIMIT %s OFFSET %s' 
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query=query, args=(page.per_page + 1, _offset(page)))
        res = await cursor.fetchall()
        if res and (len(res) > page.per_page):
            return (
                [res[i] for i in range(len(res) - 1)],
                len(res) > page.per_page,
            )
        return (res, False)


def _offset(page: PageInfo) -> int:
    if page.page <= 1:
        return 0
    else:
        return (page.page - 1) * page.per_page
