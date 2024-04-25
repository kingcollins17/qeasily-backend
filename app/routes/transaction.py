from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Any, Dict
from app import get_db
from app.dependencies.path_deps import *
from app.db.categories_crud import *
from app.models.page_request import PageInfo
from app.models.user_model import *
from app.models.plan import *
from app.utils.security import *
import math
import httpx

from app.utils.util_routes import offset, parse_list
from .transaction_util import *

transaction = APIRouter()


@transaction.post("/subscribe")
async def _subscribe(
    plan_id: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[aiomysql.Connection, Depends(get_db)],
):
    try:
        plan = find_plan(plan_id)
        if plan:
            response: Dict = await initalize_transaction(
                email=user.email, amount=math.ceil(plan.price * 100)
            )
            data = response.get("data")
            if data:
                reference = data["reference"]
                access_code = data["access_code"]
                await subscribe(
                    connection=db,
                    plan=plan,
                    user=user,
                    reference=reference,
                    access_code=access_code,
                )
            else:
                raise Exception("No response data after initalizing transaction")

            return {"detail": "Sucessful", **response}
        else:
            raise Exception(f"Could not find plan with id {plan_id}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@transaction.delete("/delete")
async def delete_transaction(
    ref: str,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        await abandon_subscription(connection=db, reference=ref)
        return {'detail': 'Transaction deleted successfully'}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')


@transaction.get("/force-verify")
async def _force_verify(
    ref: str,
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        response = await db_verify_transaction(connection=db, reference=ref)
        return {
            "detail": f"Congrats, you have bought the {response.name} package",
            "data": response,
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")


@transaction.get("/pending")
async def fetch_pending_transactions(
    db: Annotated[aiomysql.Connection, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    page: PageInfo,
):
    # try:
    async with db.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        query = """SELECT * FROM subscription_trans WHERE status = 'pending' 
            AND user_id = %s ORDER BY created_at DESC LIMIT %s OFFSET %s"""
        await cursor.execute(query, args=(user.id, page.per_page + 1, offset(page)))
        data, next = parse_list(await cursor.fetchall(), page)
        return {
            "detail": "Fetched your Pending Transactions",
            "data": data,
            "has_next_page": next,
        }


# except Exception as e:
# raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
