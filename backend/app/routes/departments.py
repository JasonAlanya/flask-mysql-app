from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models.departmentsModel import DepartmentPostModel, DepartmentUpdateModel, departments_file_types
from app.services.queryService import execute_query
from app.services.csvDataLoader import load_csv_to_db

departments_bp = Blueprint("departments", __name__)

@departments_bp.route("/", methods=["GET"])
async def get_departments():
    """
    Retrieve all departments asynchronously.

    Returns:
        Response: JSON response containing a list of departments or an error message.
    """
    result = await execute_query("SELECT * FROM departments;", fetchall=True)
    return jsonify(result), 200 if isinstance(result, list) else 500

@departments_bp.route("/<int:id>", methods=["GET"])
async def get_department(id):
    """
    Retrieve a department by ID asynchronously.

    Args:
        id (int): The ID of the department to retrieve.

    Returns:
        Response: JSON response containing the department data or an error message.
    """
    result = await execute_query("SELECT * FROM departments WHERE id = %s;", (id), fetchone=True)
    return jsonify(result) if result else jsonify({"error": "Department not found"}), 404 if not result else 200

@departments_bp.route("/", methods=["POST"])
async def create_department():
    """
    Insert a single department asynchronously.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    try:
        data = DepartmentPostModel(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
        
    result = await execute_query(
        "INSERT INTO departments (id, department) VALUES (%s, %s);", 
        (data.id, data.department)
    )
    
    if "error" in result:
        return jsonify(result), 500

    return jsonify({"message": "Department added successfully"}), 201

@departments_bp.route("/upload", methods=["POST"])
async def upload_csv_departments():
    """
    Upload a CSV file to insert multiple departments.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    query = "INSERT INTO departments (id, department) VALUES (%s, %s);"
    
    departments_expected_types = departments_file_types()
    
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    return await load_csv_to_db(file, query, departments_expected_types)

@departments_bp.route("/<int:id>", methods=["PUT"])
async def update_department(id):
    """
    Update a department asynchronously.

    Args:
        id (int): The ID of the department to update.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    try:
        data = DepartmentUpdateModel(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    result = await execute_query(
        "UPDATE departments SET department = %s WHERE id = %s;", 
        (data.department, id)
    )
    
    if "error" in result:
        return jsonify(result), 500
    if result["rows_affected"] == 0:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({"message": "Department updated successfully"}), 200

@departments_bp.route("/<int:id>", methods=["DELETE"])
async def delete_department(id):
    """
    Delete a department asynchronously.

    Args:
        id (int): The ID of the department to delete.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    result = await execute_query("DELETE FROM departments WHERE id = %s;", (id))
    
    if "error" in result:
        return jsonify(result), 500
    if result["rows_affected"] == 0:
        return jsonify({"error": "Department not found"}), 404
    return jsonify({"message": "Department deleted successfully"}), 200