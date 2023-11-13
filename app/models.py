from pydantic import BaseModel, Field
from typing import Any, List, Union


class Error(BaseModel):
    msg: str


class QuickStartConf(BaseModel):
    topics: List[int]
    total_questions: int = Field(
        default=30, description="Total number of questions for the quiz"
    )


class User(BaseModel):
    id: Union[int, None] = Field(default=None, description="ID of user")
    user_name: Union[str, None] = Field(
        default=None, description="Username is not required during login"
    )
    email: str
    password: str
    admin: Union[bool, None] = Field(
        default=False, description="Whether this user is an admin"
    )


class Topic(BaseModel):
    id: Union[int, None] = Field(default=None)
    title: str
    description: str
    category_id: int
    quiz_count: Union[int, None] = Field(default=None, description='Number of quizzes this topic has')

    

class Category(BaseModel):
    id: Union[int, None] = Field(default=None)
    name: str
    topics: Union[List[Topic], None] = Field(
        default=None, description="List of topics under this category"
    )
    topic_count: Union[int, None] = Field(
        default=None, description="The number of topics in this category"
    )

    def add_topic_count(self):
        if self.topics:
            self.topic_count = len(self.topics)
        else:
            self.topic_count = 0
        return self

    



class Question(BaseModel):
    id: Union[int, None] = Field(
        default=None, description="Integer ID is not required for insertion"
    )
    question: str
    A: str
    B: str
    C: str
    D: str
    correct: str
    explanation: str
    topic_id: Union[int, None] = Field(default=None)
    user_id: Union[int, None] = Field(default=None)

    def to_tuple(self, topic_id: int, user_id: int):
        return (
            self.question,
            self.A,
            self.B,
            self.C,
            self.D,
            self.correct,
            self.explanation,
            topic_id,
            user_id,
        )


class Quiz(BaseModel):
    id: Union[int, None] = Field(default=None)
    title: str
    questions: List[int]
    topic_id: int
    user_id: Union[int, None] = Field(default=None, description='The user_id of the user that created this quiz')
    quiz_data: Union[List[Question], None] = Field(
        default=None, description="The actual list of questions for this quiz"
    )
    duration: int

    def add_user_id(self, id: Union[int, None]):
        """Append the user id and return this object"""
        self.user_id = id
        return self



class IdList(BaseModel):
    id: List[int]
