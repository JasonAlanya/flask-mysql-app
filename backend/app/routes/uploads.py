from flask import Blueprint, request, jsonify
from app.services.csvDataLoader import load_csv_to_db

uploads_bp = Blueprint("uploads", __name__)

@uploads_bp.route("/departments", methods=["POST"])
def upload_csv_departments():
    query = '''
            INSERT INTO departments (id, department)
            VALUES (%s, %s)
        '''
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    return load_csv_to_db(file, query)

@uploads_bp.route("/jobs", methods=["POST"])
def upload_csv_jobs():
    query = '''
            INSERT INTO jobs (id, job)
            VALUES (%s, %s)
        '''
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    return load_csv_to_db(file, query)

@uploads_bp.route("/hired_employees", methods=["POST"])
def upload_csv_hired_employees():
    query = 'INSERT INTO hired_employees (id, name, datetime, department_id, job_id) VALUES (%s, %s, %s, %s, %s)'
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    return load_csv_to_db(file, query)