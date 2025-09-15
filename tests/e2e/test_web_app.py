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

def test_search_no_result(client):
    response = client.get('/browse?search=qwertyuiop')
    assert response.status_code == 200
    assert b'No Results' in response.data

def test_post_review_unauthenticated(client, auth):
    auth.login()
    response = client.delete('/recipe/7989/review/', data = {'review_id': '1234'}, follow_redirects=True)
    assert response.status_code == 200

def test_adding_duplicate_favourites(client, auth):
    auth.login()
    res_1 = client.post('/user/favourites', data = {'recipe_id' : '7989'})
    res_2 = client.post('/user/favourites', data = {'recipe_id' : '7989'})
    assert res_2.status_code == 400

def test_wrong_login_details(client, auth):
    wrong_auth_response = client.post('/auth/login', data = {'user_name': 'Not a user', 'password': 'Not a password'})
    assert wrong_auth_response.status_code == 401

