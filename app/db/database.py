import abc
from typing import Any, List, Tuple, Dict
import aiomysql
from app.models import *
from app.utils.util_functions import parse_question_list


class Database(abc.ABC):
    """All relevant Database operations for this application"""

    @staticmethod
    async def create_user(*, connection: aiomysql.Connection, user: User) -> None:
        async with connection.cursor() as cursor:
            query = "INSERT INTO users (user_name, email, password, admin) VALUES (%s,%s,%s,%s)"
            await cursor.execute(
                query, (user.user_name, user.email, user.password, user.admin)
            )
        # commit changes to database
        await connection.commit()

    @staticmethod
    async def add_category(
        *, connection: aiomysql.Connection, categories: List[Category]
    ):
        async with connection.cursor() as cur:
            cursor: aiomysql.Cursor = cur
            query = "INSERT INTO categories (name) VALUES (%s)"
            await cursor.executemany(
                query=query, args=[(cat.name,) for cat in categories]
            )

        # commit changes to db
        await connection.commit()

    @staticmethod
    async def search_category(
        *, connection: aiomysql.Connection, term: str
    ) -> List[Category] | None:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.Cursor = cursor
            query = f"SELECT * FROM categories WHERE name LIKE '%{term}%'"
            await cursor.execute(query=query)
            res = await cursor.fetchall()
            if res:
                return [Category(**value) for value in res]

    @staticmethod
    async def remove_category(*, connection: aiomysql.Connection, ids: List[int]):
        async with connection.cursor() as cursor:
            query = f"DELETE FROM categories WHERE id IN {tuple(ids)}"
            await cursor.execute(query=query)

        await connection.commit()

    @staticmethod
    async def search_topic(
        *, connection: aiomysql.Connection, search_term: str
    ) -> List[Topic] | None:
        query = f"SELECT * FROM topics WHERE title LIKE '%{search_term}%'"
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query)
            res = await cursor.fetchall()
        if len(res) < 1:
            return None

        return [Topic(**value) for value in res]

    @staticmethod
    async def add_topic(*, connection: aiomysql.Connection, topic: Topic):
        async with connection.cursor(aiomysql.Cursor) as cursor:
            query = "INSERT INTO topics (title, description, category_id) VALUES (%s, %s, %s)"
            await cursor.execute(
                query, args=(topic.title, topic.description, topic.category_id)
            )
            await connection.commit()

    @staticmethod
    async def update_topic(*, connection: aiomysql.Connection, topics: List[Topic]):
        query = "UPDATE topics SET title = %s, description = %s WHERE id = %s"
        async with connection.cursor() as cur:
            cursor: aiomysql.Cursor = cur
            await cursor.executemany(
                query=query,
                args=[(topic.title, topic.description, topic.id) for topic in topics],
            )

        await connection.commit()

    @staticmethod
    async def remove_topic(
        *, connection: aiomysql.Connection, topic_id: int | List[int]
    ):
        async with connection.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            query = "DELETE FROM topics WHERE (id = %s)"
            if isinstance(topic_id, list):
                await cursor.executemany(
                    query=query, args=[(value,) for value in topic_id]
                )
            else:
                await cursor.execute(query=query, args=(topic_id,))
            await connection.commit()

    @staticmethod
    async def update_question(
        *, connection: aiomysql.Connection, question_list: List[Question]
    ):
        query = "UPDATE questions SET question= %s, A = %s, B = %s, C = %s, D = %s WHERE id = %s"
        async with connection.cursor() as cur:
            cursor: aiomysql.Cursor = cur
            await cursor.executemany(
                query=query,
                args=[(q.question, q.A, q.B, q.C, q.D, q.id) for q in question_list],
            )
        await connection.commit()

    @staticmethod
    async def add_question(
        *, connection: aiomysql.Connection, question: Question | List[Tuple]
    ):
        query = """INSERT INTO questions (question, A, B, C, D, correct, topic_id, user_id)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        async with connection.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            if isinstance(question, list):
                await cursor.executemany(query=query, args=question)
            else:
                await cursor.execute(
                    query=query,
                    args=(
                        question.question,
                        question.A,
                        question.B,
                        question.C,
                        question.D,
                        question.correct,
                        question.topic_id,
                        question.user_id,
                    ),
                )
            await connection.commit()

    @staticmethod
    async def remove_question(
        *, connection: aiomysql.Connection, question_id: int | List[int]
    ):
        query = "DELETE FROM questions WHERE id = %s"
        async with connection.cursor() as cursor:
            cursor: aiomysql.Cursor = cursor
            if isinstance(question_id, list):
                await cursor.executemany(
                    query=query, args=[(value,) for value in question_id]
                )
            else:
                await cursor.execute(query=query, args=(question_id))
            await connection.commit()

    @staticmethod
    async def fetch_user(
        *, connection: aiomysql.Connection, id: int | str
    ) -> User | None:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = "SELECT * FROM users WHERE (id = %s OR email = %s)"
            cursor: aiomysql.DictCursor = cursor
            await cursor.execute(query, args=(id, id))
        user = await cursor.fetchone()
        if user:
            return User(**user)

    @staticmethod
    async def fetch_categories(*, connection: aiomysql.Connection, limit=50):
        query = f"SELECT * FROM categories ORDER BY id DESC LIMIT {limit}"
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query)
            res = await cursor.fetchall()

        return [Category(**value) for value in res]

    @staticmethod
    async def fetch_topics(
        *, connection: aiomysql.Connection, category_id: int, limit: int
    ):
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = f"SELECT * FROM topics WHERE (category_id = %s) ORDER BY id DESC LIMIT {limit} "
            await cursor.execute(query, args=(category_id,))
            res = await cursor.fetchall()

        return [Topic(**data) for data in res]

    @staticmethod
    async def fetch_questions(
        *,
        connection: aiomysql.Connection,
        ids: List[int] | None = None,
        topics: List[int] | None = None,
        limit: int = 100,
    ):
        query = f"SELECT * FROM questions ORDER BY id DESC LIMIT {limit}"
        res = []
        if not ids and not topics:
            raise Exception("Topic or list of ids must be provided")

        async with connection.cursor(aiomysql.DictCursor) as cur:
            cursor: aiomysql.Cursor = cur
            if ids:
                query = f"SELECT * FROM questions WHERE id IN {tuple(ids)}"
            elif topics:
                query = f"""SELECT * FROM questions WHERE topic_id IN {tuple(topics)}
                  ORDER BY id DESC LIMIT {limit}"""

            await cursor.execute(query=query)

            res = await cursor.fetchall()
            return [Question(**value) for value in res]

    @staticmethod
    async def add_quiz(*, connection: aiomysql.Connection, quiz: List[Quiz]):
        query = "INSERT INTO quiz (title, questions, user_id, topic_id) VALUES (%s,%s,%s,%s)"
        async with connection.cursor() as cur:
            cursor: aiomysql.Cursor = cur
            await cursor.executemany(
                query=query,
                args=[(q.title, str(q.questions), q.user_id, q.topic_id) for q in quiz],
            )
        await connection.commit()

    @staticmethod
    async def remove_quiz(*, connection: aiomysql.Connection, id: List[int]):
        query = f"DELETE FROM quiz WHERE id IN {tuple(id)}"
        async with connection.cursor() as cur:
            cursor: aiomysql.Cursor = cur
            await cursor.execute(query=query)

        await connection.commit()

    @staticmethod
    async def fetch_quiz(
        *,
        connection: aiomysql.Connection,
        term: str | None = None,
        topic_id: int | None = None,
        id: int | None = None
    ) -> List[Quiz]:
        query = "SELECT * FROM quiz"
        if topic_id:
            query = f"SELECT * FROM quiz WHERE topic_id = {topic_id} ORDER BY id DESC"
        elif term:
            query = f"SELECT * FROM quiz WHERE title LIKE '%{term}%' ORDER BY title ASC"
        elif id:
            query = f"SELECT * FROM quiz WHERE id = {id}"

        async with connection.cursor(aiomysql.DictCursor) as cursor:
            cursor: aiomysql.Cursor = cursor
            await cursor.execute(query=query)
            res = await cursor.fetchall()
            return [
                Quiz(
                    id=quiz["id"],
                    title=quiz["title"],
                    questions=parse_question_list(questions=quiz["questions"]),
                    user_id=quiz["user_id"],
                    topic_id=quiz["topic_id"],
                )
                for quiz in res
            ]
