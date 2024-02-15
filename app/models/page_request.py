from typing import Any, Generic,TypeVar
from pydantic import BaseModel, Field


class PageInfo(BaseModel):
    per_page: int
    page: int
