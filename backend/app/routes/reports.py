from flask import Blueprint, jsonify, request
from app.services.queryService import execute_query

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/total_hired_per_quarter", methods=["GET"])
async def get_total_hired_per_quarter():
    """
    Retrieve the total number of hired employees per quarter asynchronously.

    Returns:
        Response: JSON response containing the total number of hired employees per quarter or an error message.
    """
    result = await execute_query("SELECT count(*) AS total FROM HiredEmployeesPerQuarter;", fetchall=True)

    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result), 200 

@reports_bp.route("/hired_per_quarter", methods=["GET"])
async def get_hired_per_quarter():
    """
    Retrieve all hired_employees per quarter asynchronously.

    Returns:
        Response: JSON response containing a list of hired_employees per quarter or an error message.
    """
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page

    result = await execute_query(f"SELECT * FROM HiredEmployeesPerQuarter LIMIT {per_page} OFFSET {offset};", fetchall=True)
    
    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result), 200 

@reports_bp.route("/total_departments_above_avg", methods=["GET"])
async def get_total_departments_above_avg():
    """
    Retrieve the total number of departments with more employees than the average asynchronously.

    Returns:
        Response: JSON response containing the total number of departments or an error message.
    """
    result = await execute_query("SELECT count(*) AS total FROM DepartmentsAboveAvg;", fetchall=True)

    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result), 200 

@reports_bp.route("/departments_above_avg", methods=["GET"])
async def get_departments_above_avg():
    """
    Retrieve all departments with more employees than the average asynchronously.

    Returns:
        Response: JSON response containing a list of departments or an error message.
    """
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page

    result = await execute_query(f"SELECT * FROM DepartmentsAboveAvg LIMIT {per_page} OFFSET {offset};", fetchall=True)

    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result), 200 