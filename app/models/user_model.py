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
    
class RegisterUser(User):
    password: str

LoginUser = RegisterUser


class UserProfile(BaseModel):
    id: int | None = Field(default= None, description='Id of this user profile record')
    first_name: str
    last_name: str
    reg_no: str | None
    department: str
    level: str
    user_id: int 


