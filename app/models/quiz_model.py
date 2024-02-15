from pydantic import BaseModel, Field
from typing import Literal, List


class QuizModel(BaseModel):
    id: int | None
    title: str
    questions: List[int]
    description: str
    user_id: int
    topic_id: int
    duration: int
    qualified: Literal['Basic', 'Scholar', 'Any']
    difficulty: Literal['Easy', 'Medium', 'Hard', 'Fixed']