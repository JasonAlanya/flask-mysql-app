# Backend Documentation

## Overview
This backend is built using **Flask** and **MySQLdb** to handle data ingestion from CSV files into a MySQL database. The API provides endpoints for uploading employee data and retrieving stored records.

## Project Structure
```
backend/
┣ app/
┃ ┣ routes/            # API routes
┃ ┃ ┗ uploads.py       # Endpoints for file uploads
┃ ┣ services/          # Business logic
┃ ┃ ┗ csvDataLoader.py # CSV data processing logic
┃ ┣ utils/             # Utility functions
┃ ┃ ┣ db.py            # Database connection using pymysql
┃ ┃ ┗ helpers.py       # CSV parsing helper functions
┃ ┣ __init__.py        # App initialization
┣ .env                 # Environment variables (not committed to Git)
┣ .env.example         # Example environment variables file
┣ main.py              # Entry point for running the API
┗ requirements.txt     # Python dependences
```

## Installation
### 1. Set Up Environment
Ensure you have **Python 3** installed and set up requirments:
```sh
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in `backend/` based on `.env.example` and configure your MySQL database credentials:
```sh
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=password
DB_NAME=company_db
```
### 3. Run the API
Start the Flask application:
```sh
python main.py
```
The server will be running at `http://127.0.0.1:5000/`.

## Next Steps
- Add batch processing for expose data exploration.
- Implement unit tests.
- Containerize and deploy.


