import MySQLdb
import os

def get_db_connection():
    """
    Establishes a connection to the MySQL database.

    This function retrieves the database connection parameters from environment variables
    and uses them to create and return a connection object to the specified MySQL database.

    Returns:
        pymysql.connections.Connection: A connection object to the MySQL database.
    """

    return MySQLdb.connect( host = os.getenv("DB_HOST", "localhost"),
                            user = os.getenv("DB_USER", "root"),
                            passwd = os.getenv("DB_PASSWORD", "your_password"),
                            db = os.getenv("DB_NAME", "company_db")
                        )
