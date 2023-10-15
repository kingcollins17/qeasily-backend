from typing import Annotated, Any, List, Tuple

import aiomysql
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from pymysql.err import IntegrityError

from app import get_db
from app.db.database import Database
from app.models import *
from app.utils.util_functions import parse_csv
from app.utils.util_paths import get_current_user

route = APIRouter(dependencies=[Depends(get_current_user)])


@route.get("/categories")
async def get_categories(
    db: Annotated[aiomysql.Connection, Depends(get_db)], lim: int = 100
):
    return await Database.fetch_categories(connection=db, limit=lim)


@route.get("/topic")
async def get_topics(
    cid: int, db: Annotated[aiomysql.Connection, Depends(get_db)], lim: int = 100
):
    return await Database.fetch_topics(connection=db, category_id=cid, limit=lim)


@route.get("/quiz")
async def get_question(topic: int, db: Annotated[aiomysql.Connection, Depends(get_db)]):
    return await Database.fetch_quiz(connection=db, topic_id=topic)


@route.post("/quiz")
async def add_quiz(
    quiz: List[Quiz],
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        await Database.add_quiz(
            connection=db, quiz=[q.add_user_id(user.id) for q in quiz]
        )
        return {"detail": "Quiz objects added successfully"}

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Quiz data provided is invalid",
        )


@route.delete("/quiz/remove")
async def remove_quiz(
    id: IdList,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    # user: Annotated[User, Depends(get_current_user)],
):
    await Database.remove_quiz(connection=db, id=id.id)
    return {"detail": "Quiz objects removed"}


@route.post("/categories")
async def add_category(
    categories: List[Category],
    # user: Annotated[User, Depends(get_current_user)],
    db: Annotated[aiomysql.Connection, Depends(get_db)],
):
    await Database.add_category(connection=db, categories=categories)
    return {"details": "Added Category objects successfully"}


@route.delete("/categories/remove")
async def remove_category(
    id: IdList, db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    await Database.remove_category(connection=db, ids=id.id)
    return {"detail": "Categories removed"}


@route.post("/topic")
async def add_topic(
    topic: Topic,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User | None, Depends(get_current_user)],
):
    await Database.add_topic(connection=db, topic=topic)
    return {"detail": f"Added Topic '{topic.title}'"}


@route.delete("/topic/remove")
async def remove_topic(
    ids: IdList, db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    await Database.remove_topic(topic_id=ids.id, connection=db)
    return {"detail": f"Topics {ids.id} removed"}


@route.put("/topic/update")
async def update_topic(
    topics: List[Topic], db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    await Database.update_topic(connection=db, topics=topics)
    return {"detail": "Topic was updated"}


@route.get("/question")
async def get_questions(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    tid: int | None = None,
    qid: int | None = None,
):
    try:
        if tid:
            return await Database.fetch_questions(connection=db, topics=[tid])
        else:
            return await Database.fetch_questions(connection=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check that <topicID> or <quizId> query param is provided",
        )


@route.post("/question")
async def add_question(
    topic: int,
    data: List[Question],
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    #questions is a list of int which are question ids in the database
    questions = [(q.to_tuple(topic, user.id)) for q in data]  # type: ignore
    try:
        questions = await Database.add_question(connection=db, question=questions)
        return {"detail": "Questions added successfully", "questions": questions}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question data is invalid!",
        )
    


@route.put("/question/update")
async def update_question(
    questions: List[Question],
    # user = Annotated[User, Depends(get_current_user)]
    db: Annotated[aiomysql.Connection, Depends(get_db)],
):
    await Database.update_question(connection=db, question_list=questions)
    return {"detail": "Questions updated successfully"}


@route.post("/question/csv")
async def handle_csv_(
    topic: int,
    file: UploadFile,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    contents = await file.read()

    questions = parse_csv(contents=contents.decode(), topic_id=topic, user_id=user.id)  # type: ignore

    try:
        questions = await Database.add_question(question=questions, connection=db)
        return {"detail": "CSV Upload processed", "questions": questions}
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Error processing and adding csv questions to db",
        )
    


@route.delete("/question/remove")
async def drop_question(
    ids: IdList,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        await Database.remove_question(connection=db, question_id=ids.id)
        return {"detail": "Questions deleted successfully"}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to delete questions!",
        )
