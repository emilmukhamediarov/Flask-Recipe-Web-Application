import pytest
from pygments.lexers import q


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




def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_favourite_duplicate_add(client, auth):
    auth.login()
    client.post('/favourite/add', data={'recipe_id': 100})
    response = client.post('/favourite/add', data={'recipe_id': 100}, follow_redirects=True)
    assert b"already in favourites" in response.data

def test_browse_2nd_page(client):
    response = client.get('/browse', query_string={'page': 2})
    assert response.status_code == 200
    assert b'Black Coffee Barbecue Sauce' in response.data

def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.status_code == 200
    assert response.headers['Location'].endswith('/authentication/login')

def test_search_recipe(client):
    # response = client.get('/recipe/search?q=Low-Fat Berry Blue Frozen Dessert')
    response = client.get('/browse', query_string={'search': 'Low-Fat Berry Blue Frozen Dessert'})
    assert response.status_code == 200
    assert b'Low-Fat Berry Blue Frozen Dessert' in response.data

def test_user_can_comment(client):
    # response = client.get('/recipe/38')
    response = client.post('/recipe/38/comment', data={'text': 'Hello Frozen Dessert what are you'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Hello Frozen Dessert what are you' in response.data


def test_health_star_rating(client):
    response = client.get('/recipe/38')
    assert response.status_code == 404
    assert b'Health Star Rating 4/5' in response.data


def test_authentication_register(client):
    response = client.get('/auth/register', data={'username': 'username', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)
    assert response.status_code == 404
