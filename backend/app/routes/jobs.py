from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models.jobsModel import JobPostModel, JobUpdateModel, jobs_file_types
from app.services.queryService import execute_query
from app.services.csvDataLoader import load_csv_to_db

jobs_bp = Blueprint("jobs", __name__)

@jobs_bp.route("/", methods=["GET"])
async def get_jobs():
    """
    Retrieve all jobs asynchronously.

    Returns:
        Response: JSON response containing a list of jobs or an error message.
    """
    result = await execute_query("SELECT * FROM jobs;", fetchall=True)

    if "error" in result:
        return jsonify(result), 500
    
    return jsonify(result), 200 

@jobs_bp.route("/<int:id>", methods=["GET"])
async def get_job(id):
    """
    Retrieve a job by ID asynchronously.

    Args:
        id (int): The ID of the job to retrieve.

    Returns:
        Response: JSON response containing the job data or an error message.
    """
    result = await execute_query("SELECT * FROM jobs WHERE id = %s;", (id), fetchone=True)
    return jsonify(result) if result else jsonify({"error": "Job not found"}), 404 if not result else 200

@jobs_bp.route("/", methods=["POST"])
async def create_job():
    """
    Insert a single job asynchronously.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    try:
        data = JobPostModel(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    result = await execute_query(
        "INSERT INTO jobs (id, job) VALUES (%s, %s);", 
        (data.id, data.job)
    )
    
    if "error" in result:
        return jsonify(result), 500

    return jsonify({"message": "Job added successfully"}), 201

@jobs_bp.route("/upload", methods=["POST"])
async def upload_csv_jobs():
    """
    Upload a CSV file to insert multiple jobs.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    query = "INSERT INTO jobs (id, job) VALUES (%s, %s);"

    jobs_expected_types = jobs_file_types()

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    return await load_csv_to_db(file, query, jobs_expected_types)

@jobs_bp.route("/<int:id>", methods=["PUT"])
async def update_job(id):
    """
    Update a job by ID asynchronously.

    Args:
        id (int): The ID of the job to update.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    try:
        data = JobUpdateModel(**request.json)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    result = await execute_query(
        "UPDATE jobs SET job = %s WHERE id = %s;", 
        (data.job, id)
    )
    
    if "error" in result:
        return jsonify(result), 500
    if result["rows_affected"] == 0:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"message": "Job updated successfully"}), 200

@jobs_bp.route("/<int:id>", methods=["DELETE"])
async def delete_job(id):
    """
    Delete a job by ID asynchronously.

    Args:
        id (int): The ID of the job to delete.

    Returns:
        Response: JSON response indicating success or failure of the operation.
    """
    result = await execute_query("DELETE FROM jobs WHERE id = %s;", (id))

    if "error" in result:
        return jsonify(result), 500
    if result["rows_affected"] == 0:
        return jsonify({"error": "Job not found"}), 404
    return jsonify({"message": "Job deleted successfully"}), 200