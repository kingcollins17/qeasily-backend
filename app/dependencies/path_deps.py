
from typing import Annotated
from fastapi import Depends, HTTPException, status
from jose.exceptions import JWTError, ExpiredSignatureError
from app.models.user_model import *
from app.utils.security import decode_token, oauth_scheme

def get_current_user(token: Annotated[str, Depends(oauth_scheme)]):
    try:
        data = decode_token(token=token)
        return User(
            id=data["id"],
            user_name=data["user_name"],
            email=data["email"],
            type=data['type']
        )
    except ExpiredSignatureError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token has expired or is invalid!",
        )
    except JWTError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check that token is available or valid",
        )