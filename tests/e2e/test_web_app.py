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

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

def test_browse_2nd_page(client):
    response = client.get('/browse', query_string={'page': 2})
    assert response.status_code == 200
    assert b'Black Coffee Barbecue Sauce' in response.data

def test_search_recipe(client):
    response = client.get('/browse', query_string={'search': 'Low-Fat Berry Blue Frozen Dessert'})
    assert response.status_code == 200
    assert b'Low-Fat Berry Blue Frozen Dessert' in response.data

def test_authentication_register(client):
    response = client.get('/auth/register', data={'username': 'username', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)
    assert response.status_code == 200

def test_favourites_requires_login(client):
    response = client.get('/favourites/', follow_redirects=False)

    # Should redirect (302) to login
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/auth/login')

def test_login_required_to_comment(client):
    response = client.post('/comment')
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/authentication/login')

def test_favourite_duplicate_add(client, auth):
    auth.login()
    client.post('/favourite/add', data={'recipe_id': 101})
    response = client.post('/favourite/add', data={'recipe_id': 101}, follow_redirects=True)
    assert b"already in favourites" in response.data

def test_favourite_add_and_list(client, auth):
    auth.login()
    response = client.post('/favourite/add', data={'recipe_id': 38}, follow_redirects=True)
    assert b"Added in favourites" in response.data

    list_page = client.get('/favourites')
    assert list_page.status_code == 200
    assert b'Low-Fat Berry Blue Frozen Dessert' in list_page.data


def test_user_can_comment(client):
    response = client.post('/recipe/38/comment', data={'text': 'Hello Frozen Dessert what are you'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Hello Frozen Dessert what are you' in response.data


def test_health_star_rating(client):
    response = client.get('/recipe/38')
    assert response.status_code == 200
    assert b'Health Star Rating 4/5' in response.data



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

def test_wrong_login_details(client):
    wrong_auth_response = client.post('/auth/login', data = {'user_name': 'Not a user', 'password': 'Not a password'})
    assert wrong_auth_response.status_code == 401