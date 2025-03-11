from flask import Blueprint, jsonify
from app.services.queryService import execute_query

reports_bp = Blueprint("reports", __name__)

@reports_bp.route("/hired_per_quarter", methods=["GET"])
async def get_hired_per_quarte():
    """
    Retrieve all hired_employees per quarter asynchronously.

    Returns:
        Response: JSON response containing a list of hired_employees per quarter or an error message.
    """
    result = await execute_query("CALL GetHiredPerQuarter();;", fetchall=True)
    return jsonify(result), 200 if isinstance(result, list) else 500

@reports_bp.route("/departments_above_avg", methods=["GET"])
async def get_departments_above_avg():
    """
    Retrieve all departments with more employees than the average asynchronously.

    Returns:
        Response: JSON response containing a list of departments or an error message.
    """
    result = await execute_query("CALL GetDepartmentsAboveAvg();", fetchall=True)
    return jsonify(result), 200 if isinstance(result, list) else 500