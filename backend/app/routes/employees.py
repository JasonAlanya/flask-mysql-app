from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models.employeesModel import EmployeePostModel, EmployeeUpdateModel, employees_file_types
from app.services.queryService import execute_query
from app.services.csvDataLoader import load_csv_to_db

employees_bp = Blueprint("employees", __name__)

@employees_bp.route("/", methods=["GET"])
async def get_employees():
    """
    Retrieve all hired_employees asynchronously.

    Returns:
        Response: JSON response containing a list of employees or an error message.
    """
    result = await execute_query("SELECT * FROM hired_employees;", fetchall=True)
    return jsonify(result), 200 if isinstance(result, list) else 500

@employees_bp.route("/<int:id>", methods=["GET"])
async def get_employee(id):
    """
    Retrieve a hired_employee by ID asynchronously.

    Args:
        id (int): The ID of the hired_employee to retrieve.

    Returns:
        Response: JSON response containing the hired_employee data or an error message.
    """
    result = await execute_query("SELECT * FROM hired_employees WHERE id = %s;", (id), fetchone=True)
    return jsonify(result) if result else jsonify({"error": "Employee not found"}), 404 if not result else 200

@employees_bp.route("/", methods=["POST"])
async def create_employee():
    """
    Insert a single hired_employee asynchronously.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    try:
        data = EmployeePostModel(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    result = await execute_query(
        "INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (%s, %s, %s, %s, %s);", 
        (data.id, data.name, data.datetime, data.department_id, data.job_id)
    )
    
    if "error" in result:
        return jsonify(result), 500

    return jsonify({"message": "Employee added successfully"}), 201

@employees_bp.route("/upload", methods=["POST"])
async def upload_csv_employees():
    """
    Upload a CSV file to insert multiple employees.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    query = 'INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (%s, %s, %s, %s, %s)'
    
    employees_expected_types = employees_file_types()

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    
    return await load_csv_to_db(file, query, employees_expected_types)

@employees_bp.route("/<int:id>", methods=["PUT"])
async def update_employee(id):
    """
    Update a hired_employee by ID asynchronously.

    Args:
        id (int): The ID of the hired_employee to update.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    try:
        data = EmployeeUpdateModel(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    result = await execute_query(
        "UPDATE hired_employees SET name = %s, datetime = %s, department_id = %s, job_id = %s WHERE id = %s;", 
        (data.name, data.datetime, data.department_id, data.job_id, id)
    )
    
    if "error" in result:
        return jsonify(result), 500
    if result["rows_affected"] == 0:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee updated successfully"}), 200

@employees_bp.route("/<int:id>", methods=["DELETE"])
async def delete_employee(id):
    """
    Delete a hired_employee by ID asynchronously.

    Args:
        id (int): The ID of the hired_employee to delete.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    result = await execute_query("DELETE FROM hired_employees WHERE id = %s;", (id))
    
    if "error" in result:
        return jsonify(result), 500
    if result["rows_affected"] == 0:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify({"message": "Employee deleted successfully"}), 200