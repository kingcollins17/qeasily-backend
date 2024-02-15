from typing import Annotated
import pymysql
import aiomysql
from fastapi import Depends, HTTPException, status
import jose

from app import get_db
from app.db.database import Database
from app.db.user_crud import *
from app.models.user_model import *
from app.utils.security import verify_hash



# authentcate is a dependency for login path param
async def authenticate(
    user: LoginUser, db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    db_user = await db_find_user(connection=db, email=user.email)
    if db_user:
        try:
            if verify_hash(user.password, db_user["password"]):
                return User(
                    id=db_user["id"],
                    user_name=db_user["user_name"],
                    email=db_user["email"],
                    type=db_user["type"],
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Passwords do not match",
                )
        except jose.ExpiredSignatureError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{type(e)} error",
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {user.email} is not registered",
        )
