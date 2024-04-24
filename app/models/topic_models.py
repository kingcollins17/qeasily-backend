from pydantic import BaseModel, Field
from typing import List,Any


class Topic(BaseModel):
    id: int | None =None
    title: str
    description: str
    # date_added: str | None = None
    category_id: int
    # user_id: int

