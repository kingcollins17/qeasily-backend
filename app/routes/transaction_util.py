import httpx
import aiomysql
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Any, Dict
from app import get_db
from app.dependencies.path_deps import *
from app.db.categories_crud import *
from app.models.user_model import *
from app.models.plan import *
from app.utils.security import *

INITIALIZE_URL = "https://api.paystack.co/transaction/initialize"
VERIFY_URL = "https://api.paystack.co/transaction/verify/{reference}"
CHECKOUT_URL = "https://checkout.paystack.com/{access_code}"


async def initalize_transaction(*, email: str, amount: int):

    async with httpx.AsyncClient() as client:
        print(f"\nSending request to {INITIALIZE_URL}\n")
        response: httpx.Response = await client.post(
            url=INITIALIZE_URL,
            data={"email": email, "amount": str(amount)},
            headers={"Authorization": f"Bearer {keys.secret}"},
        )
        return response.json()


# TODO: Test this function
async def verify_transaction(*, reference):
    async with httpx.AsyncClient(
        timeout=httpx.Timeout(connect=5, read=5, write=5, pool=5)
    ) as client:
        url = VERIFY_URL.format(reference=reference)
        print("Verifying transaction at " + url)
        response: httpx.Response = await client.get(
            url,
            headers={"Authorization": f"Bearer {keys.secret}"},
        )
        return response.json()


async def subscribe(
    *,
    connection: aiomysql.Connection,
    plan: QeasilyPlan,
    user: User,
    reference: str,
    access_code: str,
):
    query0 = "INSERT INTO subscription_trans (plan, reference, access_code, user_id) VALUES (%s, %s, %s, %s)"
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query0, args=(plan.name, reference, access_code, user.id))
    await connection.commit()


async def db_verify_transaction(connection: aiomysql.Connection, reference: str):
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        query00 = "SELECT * FROM subscription_trans WHERE reference = %s"
        await cursor.execute(query00, args=(reference,))
        transaction = await cursor.fetchone()
        if transaction:
            plan: QeasilyPlan = find_plan(transaction["plan"])  # type:ignore
            await _verify(connection, reference)  # verify in db
            await renew_subscription(connection, plan, transaction["user_id"])
            await connection.commit()
            return plan
        else:
            raise Exception(f"No transaction with reference {reference} found!")


async def _verify(connection: aiomysql.Connection, reference: str):
    async with connection.cursor() as cursor:
        query = "UPDATE subscription_trans SET status = 'verified', verified_at = NOW() WHERE reference = %s"
        await cursor.execute(query, args=(reference,))


async def renew_subscription(
    connection: aiomysql.Connection, plan: QeasilyPlan, user_id: int
):
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        query00 = "UPDATE activity SET plan = %s, renewed_at = NOW(), quizzes_left = %s, admin_points = %s WHERE user_id = %s"
        await cursor.execute(query00, args=(plan.name, plan.quizzes, plan.admin_points, user_id))

        await cursor.execute(
            "UPDATE users SET type = %s WHERE id = %s", args=(plan.name, user_id)
        )


