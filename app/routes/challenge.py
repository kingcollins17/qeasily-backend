from typing import Annotated, Any, List

import aiomysql
import pymysql
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

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


class Challenge(BaseModel):
    name: str
    quizzes: List[int]
    paid: bool = False
    entry_fee: float = 0
    reward: float = 0
    duration: int = 7


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


@router.get("/created-challenges")
async def fetch_created_challenges(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:
        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(
                f"""SELECT * from challenges WHERE user_id = {user.id}
                    ORDER BY date_added ASC LIMIT {page.per_page + 1} OFFSET {_offset(page)}"""
            )
            res = await cursor.fetchall()
            if res and (len(res) > page.per_page):
                data = (
                    [res[i] for i in range(len(res) - 1)],
                    len(res) > page.per_page,
                )
            else:
                data = (res, False)
            # reuturn users creation
            if data:
                return {
                    "detail": "Your published challenges fetched",
                    "data": data[0],
                    "has_next_page": data[1],
                    "page": page,
                }
            raise Exception("No results")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get("/details")
async def get_challenge_details(
    cid: int,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        res = await _challenge_details(connection=db, challenge_id=cid, user=user)
        return {"detail": "Details fetched successfully", **res}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/start")
async def start_challenge(
    cid: int,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        await _start_challenge(connection=db, cid=cid, user=user)
        return {"detail": "You have successully entered the challenge"}
    except pymysql.IntegrityError as _:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already participating in this challenge",
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/next-task")
async def fetch_next_task(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    cid: int,
):
    try:
        res = await _fetch_next_task(connection=db, challenge_id=cid, user_id=user.id)  # type: ignore
        return {"detail": "Fetched next task", "data": res}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.post("/save-progress")
async def save_progress(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    points: int,
    cid: int,
):
    try:
        res = await _save_challenge_progress(
            connection=db,
            points=points,
            challenge_id=cid,
            user=user,
        )

        return {"detail": "Your progress has been saved. Go to next Task"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.get("/me")
async def get_current_challenges(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    """Fetches the current challenges that the user is participating"""
    try:
        query00 = f"""SELECT * FROM challenges WHERE id IN 
        (SELECT challenge_id FROM leaderboards WHERE user_id = {user.id})"""

        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(query00)
            res = await cursor.fetchall()
            return {"detail": "Your challenges fetched successfully", "data": res}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@router.post("/create")
async def add_challenge(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    challenge: Challenge,
):
    try:
        if user.is_admin == True:
            await _create_challenge(connection=db, challenge=challenge, user=user)
            return {"detail": "Challenge added successfully"}
        raise Exception(
            "You are not an admin!. Upgrade your plan to access this feature"
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/delete")
async def delete_challenge(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    cid: int,
):
    try:
        if user.is_admin() == True:
            async with db.cursor() as cursor:
                cursor: aiomysql.Cursor = cursor
                await cursor.execute(
                    f"DELETE from challenges WHERE id = {cid} AND user_id = {user.id}"
                )
            await db.commit()
            return {"detail": "Challenge deleted successfully"}
        raise Exception(
            "You are not an admin!. Upgrade your plan to access this feature"
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/leaderboards")
async def get_leaderboards(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    #     user: Annotated[User, Depends(get_current_user)],
    cid: int,
    page: PageInfo,
):
    try:
        res = await _fetch_leaderboards(connection=db, id=cid, page=page)
        return {
            "detail": f"Fetched leaderboards page {page.page} successfully",
            "data": res[0],
            "has_next_page": res[1],
            "page": page,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ---------------------------------------------------------------------------------
#
# CRUD helper functions
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def _start_challenge(*, connection: aiomysql.Connection, cid: int, user: User):
    query = """INSERT INTO leaderboards (challenge_id, user_id) VALUES (%s, %s)"""
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query, args=(cid, user.id))

    await connection.commit()


async def _save_challenge_progress(
    *, connection: aiomysql.Connection, points: int, user: User, challenge_id
):
    query00 = f"SELECT quizzes FROM challenges WHERE id = {challenge_id}"
    query01 = f"SELECT * FROM leaderboards WHERE user_id = {user.id} AND challenge_id = {challenge_id}"
    query02 = """UPDATE leaderboards SET points = points + %s, 
        progress = progress + 1 WHERE user_id = %s AND challenge_id = %s"""
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query00)
        res = await cursor.fetchone()
        quizzes = str(res["quizzes"]).removeprefix("[").removesuffix("]").split(",")

        await cursor.execute(query01)
        progress = (await cursor.fetchone())["progress"]
        # check if progress is not in range
        if progress >= len(quizzes):
            raise Exception("progress is out of range!")
        else:
            await cursor.execute(query02, args=(points, user.id, challenge_id))
            await connection.commit()


async def _fetch_next_task(
    *, connection: aiomysql.Connection, challenge_id: int, user_id: int
):

    query00 = f"SELECT quizzes FROM challenges WHERE id = {challenge_id}"
    query01 = f"SELECT progress FROM leaderboards WHERE user_id = {user_id} AND challenge_id = {challenge_id}"
    query02 = "SELECT * FROM quiz WHERE id = %s"
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query00)
        quizzes = [
            int(value)
            for value in str((await cursor.fetchone())["quizzes"])
            .removeprefix("[")
            .removesuffix("]")
            .split(",")
        ]
        # return quizzes
        await cursor.execute(query01)
        progress = (await cursor.fetchone())["progress"]

        if progress >= len(quizzes):
            raise Exception("You have completed all tasks in this challenge")

        next_task_id = quizzes[progress]
        await cursor.execute(query02, args=(next_task_id,))
        return await cursor.fetchone()


async def _fetch_leaderboards(
    *, connection: aiomysql.Connection, id: int, page: PageInfo
):
    query = """SELECT leaderboards.*, users.user_name, users.email FROM 
    leaderboards LEFT JOIN users on leaderboards.user_id = users.id WHERE challenge_id = %s LIMIT %s OFFSET %s"""

    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query, args=(id, page.per_page + 1, _offset(page)))

        res = await cursor.fetchall()
        if res and (len(res) > page.per_page):
            return (
                [res[i] for i in range(len(res) - 1)],
                len(res) > page.per_page,
            )
        return (res, False)


async def _challenge_details(
    *, connection: aiomysql.Connection, challenge_id: int, user: User
):
    query00 = f"SELECT * FROM challenges WHERE id = {challenge_id}"

    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query00)
        challenge = await cursor.fetchone()
        quizzes = [
            int(value)
            for value in str(challenge["quizzes"])
            .strip()
            .removeprefix("[")
            .removesuffix("]")
            .split(",")
        ]
        #    challenge["quizzes"] = quizzes
        query01 = f"SELECT * FROM quiz WHERE id IN {tuple(quizzes)}"
        query02 = (
            f"""SELECT COUNT(*) FROM leaderboards WHERE challenge_id = {challenge_id}"""
        )
        await cursor.execute(query01)
        quizzes = await cursor.fetchall()

        await cursor.execute(query02)
        total = await cursor.fetchone()
        return {
            "challenge": challenge,
            "quiz_data": quizzes,
            "participants": total["COUNT(*)"],
        }


async def _create_challenge(
    *, connection: aiomysql.Connection, challenge: Challenge, user: User
):
    query = """INSERT INTO challenges (name, quizzes, paid, entry_fee, reward, user_id, duration)
      VALUES (%s,%s,%s,%s,%s,%s,%s)"""
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(
            query=query,
            args=(
                challenge.name,
                str(challenge.quizzes),
                challenge.paid,
                challenge.entry_fee,
                challenge.reward,
                user.id,
                challenge.duration,
            ),
        )
    await connection.commit()


async def _fetch_challenges(
    *,
    connection: aiomysql.Connection,
    feed: bool,
    page: PageInfo,
    id: int | None = None,
):
    query = """SELECT * FROM challenges """
    if feed == True and id:
        query += f"WHERE user_id IN (SELECT followed_id FROM follows WHERE follower_id = {id}) "

    query += "ORDER BY date_added DESC LIMIT %s OFFSET %s"
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
