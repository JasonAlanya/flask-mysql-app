from flask import jsonify
from app.utils.helpers import process_csv
from app.utils.db import get_db_connection
import asyncio

async def insert_batch_into_db(cursor, query, batch, max_retries=3):
    """
    Attempts to insert a batch of data into the database with retries.

    Args:
        cursor (aiomysql.Cursor): The database cursor.
        query (str): The SQL query to execute.
        batch (list): The batch of data to insert.
        max_retries (int): The maximum number of retries in case of failure.

    Raises:
        Exception: If the maximum number of retries is reached.
    """
    for attempt in range(max_retries):
        try:
            await cursor.executemany(query, batch)
            return
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retrying batch due to error: {e}")
                await asyncio.sleep(1) 
            else:
                raise e 

async def load_csv_to_db(file, query, expected_types):
    """
    Loads a CSV file into the database asynchronously using the provided query.

    Args:
        file (file-like object): The CSV file to load.
        query (str): The SQL query to insert the data.
        expected_types (list): The expected data types for each column in the CSV.

    Returns:
        Response: A JSON response indicating the result of the operation.
    """
    try:
        data = await process_csv(file, expected_types)
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return jsonify({"error": f"Error processing CSV: {e}"}), 400
    
    if len(data) == 0:
        print("Empty or invalid CSV")
        return jsonify({"error": "Empty or invalid CSV"}), 400

    connection = await get_db_connection()
    async with connection.cursor() as cursor:
        try:
            batch_size = 1000
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                await insert_batch_into_db(cursor, query, batch) 
            await connection.commit()
        except Exception as e:
            await connection.rollback()
            print(e)
            return jsonify({"error": str(e)}), 500
        finally:
            await cursor.close()
            connection.close()

    return jsonify({"message": "CSV uploaded successfully"}), 201
