from flask import Flask
from flask_cors import CORS
from app.routes.uploads import uploads_bp
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)

    CORS(app)
    
    app.register_blueprint(uploads_bp, url_prefix="/uploads")
    
    return app