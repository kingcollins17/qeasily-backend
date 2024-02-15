from typing import Dict, Any
from pydantic import BaseModel, Field


class Category(BaseModel):
    id: int | None = None
    name: str
    user_id: int