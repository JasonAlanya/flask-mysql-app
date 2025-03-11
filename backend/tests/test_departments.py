import pytest
from app import create_app
import io

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(scope="function")
def cleanup_departments(client):
    yield
    client.delete('/departments/4535')

def test_create_department(client):
    data = {
        "id": 1,
        "department": "Supply Chain",
    }
    response = client.post('/departments/', json=data)
    assert response.status_code == 201
    assert 'message' in response.json

def test_create_department_invalid_data(client):
    data = {
        "id": "invalid_id",
        "department": "",
    }
    response = client.post('/departments/', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_departments(client):
    response = client.get('/departments/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_department(client):
    response = client.get('/departments/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_get_department_not_found(client):
    response = client.get('/departments/9999')
    assert response.status_code == 404
    assert 'error' in response.json

def test_update_department(client):
    data = {
        "department": "Maintenance",
    }
    response = client.put('/departments/1', json=data)
    assert response.status_code == 200
    assert 'message' in response.json

def test_update_department_invalid_data(client):
    data = {
        "department": 123,
    }
    response = client.put('/departments/1', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_delete_department(client):
    response = client.delete('/departments/1')
    assert response.status_code == 200
    assert 'message' in response.json

def test_delete_department_not_found(client):
    response = client.delete('/departments/9999')
    assert response.status_code == 404
    assert 'error' in response.json

def test_upload_csv_departments(client,cleanup_departments):
    data = {
        "file": (io.BytesIO(b"4535,Staff"), 'test.csv')
    }
    response = client.post('/departments/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    assert 'message' in response.json

def test_upload_csv_departments_invalid_file(client):
    data = {
        "file": (io.BytesIO(b"invalid_content,asc"), 'test.csv')
    }
    response = client.post('/departments/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.json