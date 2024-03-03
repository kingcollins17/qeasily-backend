from typing import Annotated, Any, List

import aiomysql
import pymysql
from fastapi import APIRouter, Depends, HTTPException, status

from app import get_db
from app.db.database import Database
from app.db.user_crud import *
from app.dependencies.auth_deps import authenticate
from app.dependencies.path_deps import get_current_user
from app.v_models import *
from app.models.user_model import *
from app.utils.security import *

route = APIRouter()


@route.get("/user")
async def get_user(user: Annotated[User, Depends(get_current_user)]):
    return user


@route.get("/find")
async def find_user(email: str, db: Annotated[aiomysql.Connection, Depends(get_db)]):
    user = await db_find_user(connection=db, email=email)
    if user:
        return User(
            id=user["id"],
            user_name=user["user_name"],
            email=user["email"],
            type=user["type"],
        )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not Found")


@route.post("/register")
async def register_user(
    user: RegisterUser, db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    try:
        await db_create_user(connection=db, user=user)
        return {"detail": f"User {user.email} created successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@route.post("/login")
async def login_user(user: Annotated[LoginUser, Depends(authenticate)]):
    return {"token": create_access_token(data=user.model_dump()), "user": user}


@route.get("/profile")
async def get_profile(
    id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[aiomysql.Connection, Depends(get_db)],
):
    if await db_user_has_profile(connection=db, id=id):  # type: ignore
        try:
            profile = await db_fetch_user_profile(connection=db, user_id=id)  # type: ignore
            return {"detail": f'User profile {profile["reg_no"]}', "profile": profile}  # type: ignore

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong"
            )

    else:
        # return {"detail": "User does not have any profile"}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Profile not found"
        )


@route.post("/profile/create", dependencies=[Depends(oauth_scheme)])
async def create_user_profile(
    profile: UserProfile,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
):
    try:
        await db_create_user_profile(connection=db, profile=profile)
        return {"detail": "Profile created successfully", "profile": profile}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to create User Profile",
        )


@route.put("/profile/update", dependencies=[Depends(get_current_user)])
async def has_profile(
    profile: UserProfile, db: Annotated[aiomysql.Connection, Depends(get_db)]
):
    # return {'detail': await db_user_has_profile(connection=db, id=id)}
    try:
        await db_update_user_profile(connection=db, profile=profile)
        return {"detail": "Profile updated", "new_profile": profile}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to update profile"
        )
