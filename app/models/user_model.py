# user models
from typing import Any, Union
# from fastapi import Fi
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Union[int, None] = Field(default=None, description="ID of user")
    user_name: Union[str, None] = Field(
        default=None, description="Username is not required during login"
    )
    email: str
    type: Union[str, None] = Field(
        default="Basic", description="The type of user"
    )

    def is_admin(self) -> bool:
        return self.type == 'Admin'


class RegisterUser(User):
    password: str
    department: str
    level: str


class UserProfile(BaseModel):
    department: str
    level: str


class LoginUser(BaseModel):
    email: str
    password: str


