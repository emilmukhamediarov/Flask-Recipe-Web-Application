import pytest
from recipe.favourites import services
import recipe.adapters.repository as repo
from tests.conftest import AuthenticationManager
from flask import session
import recipe.auth.services as auth_services

# --- Register and login and logout functionality  ---
def test_register_creates_user(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",  # must match password
        },
        follow_redirects=True,
    )

    assert b"Registration successful" in response.data
    user = auth_services.retrieve_user_by_name("newuser", repo.repo_instance)
    assert user is not None
    assert user.check_password("Helloworld1")

def test_login(client, auth):
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",  # must match password
        },
        follow_redirects=True,
    )
    with client:
        auth.login()
        assert session['username'] == 'newuser'
        assert session['user_id'] is not None

def test_logout(client, auth):
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",  # must match password
        },
        follow_redirects=True,
    )
    with client:
        auth.login()
        auth.logout()
        assert 'user_id' not in session

# --- Home page Web App ---
def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'We just love making recipe websites.' in response.data

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Home' in response.data

# --- Browse page Web App ---
def test_browse_without_parameters(client):
    response = client.get('/browse')
    assert response.status_code == 200
    assert b'Browse recipes:' in response.data

def test_browse_with_category(client):
    response = client.get('/browse?category=Chicken')
    assert response.status_code == 200
    assert b'Warm Chicken A La King' in response.data

def test_browse_with_author(client):
    response = client.get('/browse?author=Dancer')
    assert response.status_code == 200
    assert b'Low-Fat Berry Blue Frozen Dessert' in response.data

def test_browse_2nd_page(client):
    response = client.get('/browse', query_string={'page': 2})
    assert response.status_code == 200
    assert b'Black Coffee Barbecue Sauce' in response.data

def test_search_recipe(client):
    response = client.get('/browse', query_string={'search': 'Low-Fat Berry Blue Frozen Dessert'})
    assert response.status_code == 200
    assert b'Low-Fat Berry Blue Frozen Dessert' in response.data

def test_search_no_result(client):
    response = client.get('/browse?search=qqqqq&sort=&category=&author=')
    assert response.status_code == 200
    assert b'No results found.' in response.data

# --- Recipe Details page Web App ---
def test_recipe_details(client):
    response = client.get('/recipe/232')
    assert response.status_code == 200
    assert b'Chocolate Cream Meringue Pie' in response.data
    assert b'Nutritional Values' in response.data

def test_health_star_rating(client):
    response = client.get('/recipe/13115')
    assert response.status_code == 200
    assert b'Insufficient data for Health Score' in response.data


# --- Authentication ---
def test_authentication_register(client):
    response = client.get('/auth/register', data={'username': 'username', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)
    assert response.status_code == 200

def test_favourites_requires_login(client):
    response = client.get('/favourites/', follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['Location'].endswith('/auth/login')

def test_new_user_opens_favourites(client):
    client.post(
        '/auth/register',
        data={'username': 'newuser', 'password': 'password', 'confirm_password': 'password'},
        follow_redirects=True
    )
    response = client.get('/favourites/', follow_redirects=True)
    assert response.status_code == 200



def test_wrong_login_details(client):
    response = client.post(
        '/auth/login',
        data={'username': 'Not a user', 'password': 'Not a password'},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data



# --- Favourite Functionality ---
# --- Can add, remove, view favourites and show none if empty ---
def test_favourite_add(client, auth):
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",  # must match password
        },
        follow_redirects=True,
    )
    with client:
        auth.login()

        response = client.post(
            "/favourites/",
            data={"recipe_id": 38},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Favourite has been added" in response.data


def test_favourite_remove(client, auth):
    response = client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",  # must match password
        },
        follow_redirects=True,
    )
    with client:
        auth.login()

        response = client.post(
            "/favourites/",
            data={"recipe_id": 38},
            follow_redirects=True
        )
        assert response.status_code == 200

        response = client.post(
            "/favourites/remove",
            data={"recipe_id": 38},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Favourite has been removed" in response.data

def test_view_favourite_recipe(client, auth):
    client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",
        },
        follow_redirects=True,
    )

    with client:
        auth.login()
        assert session["username"] == "newuser"

        response = client.post(
            "/favourites/",
            data={"recipe_id": 13107},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Favourite has been added" in response.data

        response = client.get("/favourites/")
        assert response.status_code == 200

        assert b"Sauteed Scallops" in response.data

def test_empty_favourites_page(client, auth):
    client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",
        },
        follow_redirects=True,
    )

    with client:
        auth.login()
        assert session["username"] == "newuser"

        response = client.get("/favourites/")
        assert response.status_code == 200

        assert b"No favourites yet" in response.data


# --- Review Functionality ---
# --- user can post one review per recipe ---
def test_post_review(client, auth):
    client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",
        },
        follow_redirects=True,
    )
    with client:
        auth.login()
        assert session["username"] == "newuser"

        response = client.post(
            "/review",
            data={
                "recipe_id": 38,
                "rating": 5,
                "text": "This recipe is amazing!"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Review successfully submitted" in response.data

def test_duplicate_review(client, auth):
    client.post(
        "/auth/register",
        data={
            "username": "newuser",
            "password": "Helloworld1",
            "confirm": "Helloworld1",
        },
        follow_redirects=True,
    )

    with client:
        auth.login()
        assert session["username"] == "newuser"

        response = client.post(
            "/review",
            data={
                "recipe_id": 38,
                "rating": 5,
                "text": "Great recipe!"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"Review successfully submitted" in response.data

        response = client.post(
            "/review",
            data={
                "recipe_id": 38,
                "rating": 4,
                "text": "Trying to submit again"
            },
            follow_redirects=True
        )

        assert response.status_code == 200
        assert b"You have already reviewed this recipe" in response.data







