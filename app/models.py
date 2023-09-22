from pydantic import BaseModel, Field
from typing import Any, List


class Error(BaseModel):
    msg: str

class QuickStartConf(BaseModel):
    topics: List[int]
    total_questions: int = Field(default=30, description="Total number of questions for the quiz")

class User(BaseModel):
    id: int | None = Field(default=None, description="ID of user")
    user_name: str | None = Field(
        default=None, description="Username is not required during login"
    )
    email: str
    password: str
    admin: bool | None = Field(
        default=False, description="Whether this user is an admin"
    )


class Topic(BaseModel):
    id: int | None = Field(default=None)
    title: str
    description: str
    category_id: int


class Category(BaseModel):
    id: int | None = Field(default=None)
    name: str
    topics: List[Topic] | None = Field(
        default=None, description="List of topics under this category"
    )


class Question(BaseModel):
    id: int | None = Field(
        default=None, description="Integer ID is not required for insertion"
    )
    question: str
    A: str
    B: str
    C: str
    D: str
    correct: str
    topic_id: int | None = Field(default=None)
    user_id: int | None = Field(default=None)


    def to_tuple(self, topic_id: int, user_id: int):
        return (
            self.question,
            self.A,
            self.B,
            self.C,
            self.D,
            self.correct,
            topic_id,
            user_id,
        )


class Quiz(BaseModel):
    id: int | None = Field(default=None)
    title: str
    questions: List[int]
    topic_id: int 
    user_id: int 
    quiz_data: List[Question] | None = Field(
        default=None, description="The actual list of questions for this quiz"
    )


class IdList(BaseModel):
    id: List[int]
