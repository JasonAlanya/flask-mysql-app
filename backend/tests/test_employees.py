import pytest
from app import create_app
import io

@pytest.fixture(scope="module") 
def app():
    app = create_app()
    return app

@pytest.fixture(scope="module")
def client(app):
    return app.test_client()

@pytest.fixture(scope="module")
def create_and_delete_entries(client):
    print("Creating entries")
    data_job = {
        "id": 1,
        "job": "Recruiter",
    }
    response = client.post('/jobs/', json=data_job)
    assert response.status_code == 201
    assert 'message' in response.json

    data_department = {
        "id": 1,
        "department": "Supply Chain",
    }
    response = client.post('/departments/', json=data_department)
    assert response.status_code == 201
    assert 'message' in response.json

    yield

    client.delete('/jobs/1')
    client.delete('/departments/1')  # Corregido el error tipográfico

    print("Deleting entries")

@pytest.fixture(scope="function")
def cleanup_employees(client):
    yield
    client.delete('/employees/4535')

def test_create_employee(client, create_and_delete_entries):
    data = {
        "id": 1,
        "name": "John Doe",
        "datetime": "2025-03-09T12:00:00Z",
        "department_id": 1,
        "job_id": 1
    }
    response = client.post('/employees/', json=data)
    assert response.status_code == 201
    assert 'message' in response.json

def test_create_employee_invalid_data(client):
    data = {
        "id": "invalid_id",
        "name": "",
        "datetime": "invalid_date",
        "department_id": "invalid_department",
        "job_id": "invalid_job"
    }
    response = client.post('/employees/', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_employees(client, create_and_delete_entries):
    response = client.get('/employees/', query_string={'page': 1, 'per_page': 10})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_employee(client, create_and_delete_entries):
    response = client.get('/employees/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_get_employee_not_found(client):
    response = client.get('/employees/9999')
    assert response.status_code == 404
    assert 'error' in response.json

def test_update_employee(client, create_and_delete_entries):
    data = {
        "name": "Jane Doe",
        "datetime": "2025-03-09T12:00:00Z",
        "department_id": 1,
        "job_id": 1
    }
    response = client.put('/employees/1', json=data)
    assert response.status_code == 200
    assert 'message' in response.json

def test_update_employee_invalid_data(client):
    data = {
        "name": "",
        "datetime": "invalid_date",
        "department_id": "invalid_department",
        "job_id": "invalid_job"
    }
    response = client.put('/employees/1', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_delete_employee(client, create_and_delete_entries):
    response = client.delete('/employees/1')
    assert response.status_code == 200
    assert 'message' in response.json

def test_delete_employee_not_found(client):
    response = client.delete('/employees/9999')
    assert response.status_code == 404
    assert 'error' in response.json

def test_upload_csv_employees(client, create_and_delete_entries, cleanup_employees):
    data = {
        "file": (io.BytesIO(b"4535,Marcelo Gonzalez,2021-07-27T16:02:08Z,1,1"), 'test.csv')
    }
    response = client.post('/employees/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    assert 'message' in response.json

def test_upload_csv_employees_invalid_file(client):
    data = {
        "file": (io.BytesIO(b"invalid_content,asc,asd,asd,asd"), 'test.csv')
    }
    response = client.post('/employees/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.json
