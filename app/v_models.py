from pydantic import BaseModel, Field
from typing import Any, List, Union


class Error(BaseModel):
    msg: str


class QuickStartConf(BaseModel):
    topics: List[int]
    total_questions: int = Field(
        default=30, description="Total number of questions for the quiz"
    )



# class Topic(BaseModel):
#     id: Union[int, None] = Field(default=None)
#     title: str
#     description: str
#     category_id: int
   



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
