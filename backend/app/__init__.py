from flask import Flask
from flask_cors import CORS
from app.routes.departments import departments_bp
from app.routes.jobs import jobs_bp
from app.routes.employees import employees_bp
from app.routes.reports import reports_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    CORS(app)
    
    app.register_blueprint(departments_bp, url_prefix="/departments")
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(employees_bp, url_prefix="/employees")
    app.register_blueprint(reports_bp, url_prefix="/reports")

    return app