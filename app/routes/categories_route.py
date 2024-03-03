from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Any, Dict
import aiomysql
from app import get_db
from app.dependencies.path_deps import *
from app.db.categories_crud import *
from app.models.user_model import *
from app.utils.security import *


cats_router = APIRouter()


@cats_router.get("/")
async def get_categories(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
):
    try:
        res = await db_fetch_categories(connection=db)  # type: ignore
        return {"detail": "categories fetched", "data": res}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to fetch categories {type(e)}",
        )


@cats_router.post("/create", dependencies=[Depends(oauth_scheme)])
async def add_categories(
    db: Annotated[aiomysql.Connection, Depends(get_db)], categories: List[Category]
):
    try:
        res = await db_add_categories(connection=db, categories=categories)
        return {"detail": "Categories added successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to add categories: {type(e)}",
        )


@cats_router.put("/update", dependencies=[Depends(oauth_scheme)])
async def update_category(
    db: Annotated[aiomysql.Connection, Depends(get_db)], category: Category
):
    try:
        res = await db_update_category(connection=db, category=category)
        return {"detail": "Categories update successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to update category {type(e)}",
        )


@cats_router.delete("/delete")
async def delete_category(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    id: int,
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        await db_delete_category(connection=db, id=id, user_id=user.id)  # type: ignore
        return {"detail": f"Category {id} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unable to delete category: {type(e)}",
        )
