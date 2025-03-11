# Backend API Documentation

## Overview
This backend is a REST API built with Flask, using asynchronous execution with `asyncio` and `aiomysql`. It provides CRUD operations for departments, jobs, and hired employees, and includes endpoints for reports. The API supports data insertion via individual requests and CSV file uploads.

## Folder Structure
```
backend/
┣ app/
┃ ┣ models/               # Pydantic models for request validation
┃ ┣ routes/               # API endpoints
┃ ┣ services/             # Database queries and CSV processing logic
┃ ┣ utils/                # Database connection and helper functions
┃ ┣ requirements.txt      # Project dependencies
┃ ┗ __init__.py           # App initialization
┣ tests/                  # Unit tests for the API
┣ .env                    # Environment variables
┣ dockerfile              # Docker configuration for containerizing the API
┣ main.py                 # API entry point
┗ README.md               # Documentation
```

## Installation & Setup

### 1. Set up a virtual environment
```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 2. Install dependencies
```sh
pip install -r app/requirements.txt
```

### 3. Configure environment variables
Copy `.env.example` to `.env` and update the values:

### 4. Run the API
```sh
python main.py
```

The API will start at `http://127.0.0.1:5000/`.

## API Endpoints

### Departments
| Method | Endpoint                | Description |
|--------|-------------------------|-------------|
| GET    | `/departments/`         | Get all departments |
| GET    | `/departments/<id>`     | Get a specific department |
| POST   | `/departments/`         | Create a new department |
| POST   | `/departments/upload`   | Upload a CSV file with departments |
| PUT    | `/departments/<id>`     | Update a department |
| DELETE | `/departments/<id>`     | Delete a department |

### Jobs
| Method | Endpoint       | Description |
|--------|---------------|-------------|
| GET    | `/jobs/`      | Get all jobs |
| GET    | `/jobs/<id>`  | Get a specific job |
| POST   | `/jobs/`      | Create a new job |
| POST   | `/jobs/upload` | Upload a CSV file with jobs |
| PUT    | `/jobs/<id>`  | Update a job |
| DELETE | `/jobs/<id>`  | Delete a job |

### Employees
| Method | Endpoint                   | Description |
|--------|-----------------------------|-------------|
| GET    | `/employees/`               | Get all employees |
| GET    | `/employees/<id>`           | Get a specific employee |
| POST   | `/employees/`               | Create a new employee |
| POST   | `/employees/upload`         | Upload a CSV file with employees |
| PUT    | `/employees/<id>`           | Update an employee |
| DELETE | `/employees/<id>`           | Delete an employee |

### Reports
| Method | Endpoint                         | Description |
|--------|-----------------------------------|-------------|
| GET    | `/reports/hired_per_quarter`     | Get number of employees hired per quarter in 2021 |
| GET    | `/reports/departments_above_avg` | Get departments with hires above average |

## Running Tests
To run unit tests, use:
```sh
pytest tests/
```

## Docker Setup
To build and run the API as a Docker container:
```sh
docker build -t my-company-flask-api .
docker run --name backend-container --env-file .env -p 5000:5000 -d my-company-flask-api
```