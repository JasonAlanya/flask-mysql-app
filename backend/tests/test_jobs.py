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
def cleanup_jobs(client):
    yield
    client.delete('/jobs/4535')

def test_create_job(client):
    data = {
        "id": 1,
        "job": "Recruiter",
    }
    response = client.post('/jobs/', json=data)
    assert response.status_code == 201
    assert 'message' in response.json

def test_create_job_invalid_data(client):
    data = {
        "id": "invalid_id",
        "job": "",
    }
    response = client.post('/jobs/', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_get_jobs(client):
    response = client.get('/jobs/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_job(client):
    response = client.get('/jobs/1')
    assert response.status_code == 200
    assert 'id' in response.json

def test_get_job_not_found(client):
    response = client.get('/jobs/9999')
    assert response.status_code == 404
    assert 'error' in response.json

def test_update_job(client):
    data = {
        "job": "Manager",
    }
    response = client.put('/jobs/1', json=data)
    assert response.status_code == 200
    assert 'message' in response.json

def test_update_job_invalid_data(client):
    data = {
        "job": 123,
    }
    response = client.put('/jobs/1', json=data)
    assert response.status_code == 400
    assert 'error' in response.json

def test_delete_job(client):
    response = client.delete('/jobs/1')
    assert response.status_code == 200
    assert 'message' in response.json

def test_delete_job_not_found(client):
    response = client.delete('/jobs/9999')
    assert response.status_code == 404
    assert 'error' in response.json

def test_upload_csv_jobs(client,cleanup_jobs):
    data = {
        "file": (io.BytesIO(b"4535,Staff"), 'test.csv')
    }
    response = client.post('/jobs/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    assert 'message' in response.json

def test_upload_csv_jobs_invalid_file(client):
    data = {
        "file": (io.BytesIO(b"invalid_content,asc"), 'test.csv')
    }
    response = client.post('/jobs/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'error' in response.json