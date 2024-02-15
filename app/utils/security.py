import os
from datetime import datetime, timedelta
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from jose import  jwt
from passlib.context import CryptContext
from app.v_models import *

### SECRET = "d116f8ed3248bf934cf19812e4f105eee20f0a067a92062b408e35ef731a8b64"
SECRET = os.getenv("SECRET_KEY", "d116f8ed3248bf934cf198")
ALGORITHM = "HS256"
context = CryptContext(schemes=["bcrypt"])

oauth_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")



def hash_password(password: str) -> str:
    return context.hash(password)


def verify_hash(plain: str, hashed: str) -> bool:
    return context.verify(plain, hashed)


def create_access_token(
    *, data: dict[str, Any], expires: timedelta = timedelta(weeks=5)
):
    copied = data.copy()
    exp = datetime.utcnow() + expires
    copied.update({"exp": exp})
    return jwt.encode(copied, key=SECRET, algorithm=ALGORITHM)


def decode_token(*, token: str) -> dict[str, Any]:
    return jwt.decode(token, SECRET, algorithms=[ALGORITHM])