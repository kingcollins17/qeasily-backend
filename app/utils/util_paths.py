import os
from datetime import datetime, timedelta
from typing import Annotated, Any, List, Tuple

import aiomysql
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError
from passlib.context import CryptContext

from app import get_db
from app.db.database import Database
from app.models import *

# SECRET = "d116f8ed3248bf934cf19812e4f105eee20f0a067a92062b408e35ef731a8b64"
SECRET = os.getenv("SECRET_KEY","d116f8ed3248bf934cf198")
ALGORITHM = "HS256"
context = CryptContext(schemes=["bcrypt"])

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# authentcate is a dependency for login path param
async def authenticate(user: User, db: Annotated[aiomysql.Connection, Depends(get_db)]):
    db_user = await Database.fetch_user(connection=db, id=user.email)
    if db_user:
        if verify_hash(user.password, db_user.password):
            # remove the user password to avoid returning it to the client
            db_user.password = ""
            return db_user
        else:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail="Password does not match",
            )


def hash_password(password: str) -> str:
    return context.hash(password)


def verify_hash(plain: str, hashed: str) -> bool:
    return context.verify(plain, hashed)


def create_access_token(
    *, data: dict[str, Any], expires: timedelta = timedelta(minutes=30)
):
    copied = data.copy()
    exp = datetime.utcnow() + expires
    copied.update({"exp": exp})
    return jwt.encode(copied, key=SECRET, algorithm=ALGORITHM)


def decode_token(*, token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])


def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    try:
        data = decode_token(token=token)
        return User(
            id=data["id"],
            user_name=data["user_name"],
            email=data["email"],
            password=data["password"],
            admin=data["admin"],
        )
    except ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired or is invalid!",
        )
    except JWTError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Check that token is available or valid")
