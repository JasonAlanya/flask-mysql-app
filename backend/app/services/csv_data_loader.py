from flask import jsonify
from app.utils.helpers import process_csv
from app.utils.db import get_db_connection

def load_csv_to_db(file, query):
    """
    Carga un archivo CSV en la base de datos utilizando la consulta proporcionada.
    
    Args:
        file (file-like object): El archivo CSV a cargar.
        query (str): La consulta SQL para insertar los datos.
    
    Returns:
        Response: Una respuesta JSON indicando el resultado de la operación.
    """
    data = process_csv(file)
    
    if len(data) == 0:
        return jsonify({"error": "Empty or invalid CSV"}), 400
    
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        batch_size = 1000
        for i in range(0, len(data), batch_size):
            batch = data[i:i + batch_size]
            cursor.executemany(query, batch)
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
    
    return jsonify({"message": "CSV uploaded successfully"}), 201