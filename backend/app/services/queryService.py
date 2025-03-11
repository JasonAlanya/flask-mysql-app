from app.utils.db import get_db_connection
import aiomysql

async def execute_query(query, params=None, fetchall=False, fetchone=False):
    """
    Helper function to execute asynchronous database queries.

    Args:
        query (str): The SQL query to execute.
        params (tuple, optional): The parameters to use with the SQL query. Defaults to None.
        fetchall (bool, optional): Whether to fetch all results. Defaults to False.
        fetchone (bool, optional): Whether to fetch a single result. Defaults to False.

    Returns:
        result (list or dict or None): The query result, either a list of rows, a single row, or None.
        If an error occurs, returns a dictionary with the error message.
    """
    connection = None
    try:
        connection = await get_db_connection()
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(query, params or ())
            print(cursor.rowcount)
            if fetchall:
                result = await cursor.fetchall()
            elif fetchone:
                result = await cursor.fetchone()
            else:
                result = {"message": "Query executed successfully", "rows_affected": cursor.rowcount}
            await connection.commit()
        return result
    except Exception as e:
        return {"error": str(e)}
    finally:
        if connection:
            connection.close()