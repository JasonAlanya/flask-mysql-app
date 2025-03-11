import aiomysql
import os
import asyncio

async def get_db_connection():
    """
    Establishes a connection to the MySQL database asynchronously.

    This function retrieves the database connection parameters from environment variables
    and uses them to create and return a connection object to the specified MySQL database.

    Returns:
        aiomysql.Connection: A connection object to the MySQL database.
    """
    
    return await aiomysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "your_password"),
        db=os.getenv("DB_NAME", "companydb"),
        loop=asyncio.get_event_loop()
    )