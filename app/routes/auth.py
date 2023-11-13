from typing import Annotated, Any, List

import aiomysql
from fastapi import APIRouter, Depends, HTTPException, status

from app import get_db
from app.db.database import Database
from app.models import *
from app.utils.util_paths import *

route = APIRouter()

@route.post("/register")
async def register_user(
    user: User, db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    if user.user_name:
        try:
            await Database.create_user(
                connection=db,
                user=User(
                    user_name=user.user_name,
                    email=user.email,
                    password=hash_password(user.password),
                    admin=user.admin,
                ),
            )
            return {'msg': f'User Account created'}
        except Exception as e:
            print(e)
            return Error(msg='Unable to create user account')


@route.post("/login")
async def login_user(user: Annotated[ Union[User, None], Depends(authenticate)]):
    if user:
            return {'token': create_access_token(data=user.model_dump())}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=Error(msg='User not found').msg)
