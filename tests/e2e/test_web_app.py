import pytest

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'We just love making recipe websites.' in response.data

def test_browse_without_parameters(client):
    response = client.get('/browse')
    assert response.status_code == 200
    assert b'Browse recipes:' in response.data

def test_browse_with_category(client):
    response = client.get('/browse?category=Bass')
    assert response.status_code == 200
    assert b'Steamed Sea Bass' in response.data

def test_browse_with_author(client):
    response = client.get('/browse?author=Annie+H')
    assert response.status_code == 200
    assert b'Grilled Chicken Breasts' in response.data

def test_recipe_details(client):
    response = client.get('/recipe/7989')
    assert response.status_code == 200
    assert b'Unstuffed Mushroom Dip' in response.data
    assert b'Nutritional Values' in response.data