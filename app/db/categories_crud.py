from typing import Dict, Any, List
import aiomysql
from app.models.categories_models import *

### - 
async def db_fetch_categories(*, connection: aiomysql.Connection):
    """Fetch <limit> categories records from db starting from <start> """
    query = f"SELECT id, name FROM categories" 
    async with connection.cursor(aiomysql.DictCursor) as cursor:
        cursor: aiomysql.DictCursor = cursor
        await cursor.execute(query=query)
     #    return (await cursor.fetchall(), await cursor.nextset())
        categories =  await cursor.fetchall()
        return categories



### - add a category to database
async def db_add_categories(*, connection: aiomysql.Connection, categories: List[Category]):
    length = len(categories)
    values = ""
    for i in range(len(categories)):
        values += f"('{categories[i].name}', {categories[i].user_id})"
        if i < (length - 1):
            values += ','
     
    query = f"INSERT INTO categories (name, user_id) VALUES {values}"
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor  = cursor
        await cursor.execute(query=query)

    await connection.commit()
        
### -  
async def db_update_category(*, connection: aiomysql.Connection, category: Category):
    if category.id:
         query = "UPDATE categories SET name = %s WHERE id = %s"
         async with connection.cursor() as cursor:
             cursor: aiomysql.Cursor = cursor
             await cursor.execute(query, args=(category.name, category.id))

         await connection.commit()
         return True
    #
    return False

### - 
async def db_delete_category(*, connection: aiomysql.Connection, id: int, user_id: int):
    """id is the category id"""
    query = f"DELETE FROM categories WHERE id = {id} AND user_id = {user_id}"
    async with connection.cursor() as cursor:
        cursor: aiomysql.Cursor = cursor
        await cursor.execute(query)
     
    await connection.commit() 