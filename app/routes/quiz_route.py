import aiomysql

from fastapi import Depends, APIRouter, HTTPException, status

from app import get_db
from app.dependencies.path_deps import *
from app.utils.util_routes import *
from app.models.user_model import *
from app.db.quiz_crud import *


quiz_router = APIRouter()


class QuizData(BaseModel):
    title: str
    questions: List[int]
    topic_id: int
    duration: int
    description: str
    difficulty: str
    type: str


@quiz_router.get("")
async def fetch_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)], page: PageInfo, topic: int
):
    # """Fetch quizzes related to a topic"""
    try:
        res = await _fetch_quiz(connection=db, page=page, topic_id=topic)
        if res:
            return {
                "detail": "Fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
        raise Exception("No result")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@quiz_router.get("/all")
async def fetch_all_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    res = await _fetch_quiz(connection=db, page=page)
    return {
        "detail": "Fetched successfully",
        "data": res[0],
        "has_next_page": res[1],
        "page": page,
    }
    # return


@quiz_router.get("/by-category")
async def fetch_from_category(
    cid: int,
    page: PageInfo,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    # level: str | None = None,
):
    """Fetch quizzes based on a broad categoriy"""
    try:
        res = await _fetch_quiz(connection=db, page=page, category_id=cid)
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
        res = await _fetch_quiz(connection=db, page=page, suggested=True,user_id=user.id)
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


@quiz_router.get("/created-quiz")
async def fetch_user_created_quizzes(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    try:
        query00 = """SELECT quiz.*, topics.title as topic, users.user_name as creator FROM quiz 
        LEFT JOIN topics ON quiz.topic_id = topics.id
        LEFT JOIN users ON quiz.user_id = users.id
        WHERE quiz.user_id = %s ORDER BY date_added DESC LIMIT %s OFFSET %s"""
        async with db.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(
                query00, args=(user.id, page.per_page + 1, offset(page))
            )
            res = parse_list((await cursor.fetchall()), page)
            return {
                "detail": "Created Quizzes fetched successfully",
                "data": res[0],
                "has_next_page": res[1],
                "page": page,
            }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@quiz_router.post("/create")
async def create_quiz(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    quiz: QuizData,
):

    try:
        query = """INSERT INTO quiz (title, questions, user_id, 
        topic_id, duration, description, difficulty, type) 
        VALUES (%s, %s, %s,%s,%s,%s,%s,%s)"""
        async with db.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.execute(
                query,
                args=(
                    quiz.title,
                    str(quiz.questions),
                    user.id,
                    quiz.topic_id,
                    quiz.duration,
                    quiz.description,
                    quiz.difficulty,
                    quiz.type,
                ),
            )
            await consume_points(db, 3, user.id) #type: ignore
            await db.commit()
        return {"detail": "Quiz created successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


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
        await consume_points(db, 1, user.id) #type: ignore
        await db.commit()
        return {"detail": "Quiz deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#
# CRUD HELPER FUNCTIONS FOR QUIZ ROUTE
# -----------------------------------------------------------------------------


async def _fetch_quiz(
    *,
    connection: aiomysql.Connection,
    page: PageInfo,
    topic_id: int | None = None,
    suggested: bool = False,
    user_id: int | None = None,
    category_id: int | None = None,
):

    query00 = """SELECT quiz.*, users.user_name as creator, topics.title as topic FROM quiz
      LEFT JOIN users ON users.id = quiz.user_id
      LEFT JOIN topics on quiz.topic_id = topics.id
      {condition} ORDER BY quiz.date_added DESC LIMIT %s OFFSET %s """
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        final_query = ""

        if topic_id:
            final_query = query00.format(condition=f" WHERE quiz.topic_id = {topic_id}")

        elif category_id:
            final_query = query00.format(
                condition=f" WHERE quiz.topic_id IN (SELECT id from topics WHERE category_id = {category_id})"
            )
        elif suggested == True and user_id:
            final_query = query00.format(
                condition=f" WHERE quiz.user_id IN (SELECT followed_id FROM follows WHERE follower_id = {user_id})"
            )
        else:
            final_query = query00.format(condition=f" ")

        await cursor.execute(
            final_query,
            args=(
                page.per_page + 1,
                offset(page),
            ),
        )
        return parse_list(await cursor.fetchall(), page)
