import pytest

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'We just love making recipe websites.' in response.data

def test_browse_without_parameters(client):
    response = client.get('/browse')
    assert response.status_code == 200
    assert b'Browse recipes:' in response.data
