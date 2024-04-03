# test_app.py
import pytest
import os
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_files(client):
    # Adjust the path to the file to match its actual location
    file_path = os.path.join('project', 'dummy_data_file', 'files.tar.gz')
    data = {
        'files[]': (open(file_path, 'rb'), 'files.tar.gz')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    assert response.headers['Content-Disposition'] == 'attachment; filename=output.tar.gz'


def test_missing_files(client):
    data = {
        'files[]': ''
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'No files selected' in response.data

# Add more test cases as needed
