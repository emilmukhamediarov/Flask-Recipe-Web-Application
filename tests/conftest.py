import pytest

from recipe import create_app
from recipe.adapters.memory_repository import MemoryRepository, populate
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite

from utils import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    test_repo = MemoryRepository()
    populate(TEST_DATA_PATH, test_repo)
    return test_repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,                                # Set to True during testing.
        'TEST_DATA_PATH': TEST_DATA_PATH,               # Path for loading test data into the repository.
        'WTF_CSRF_ENABLED': False                       # test_client will not send a CSRF token, so disable validation.
    })

    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username="newuser", password="Helloworld1", follow_redirects=True):
        return self._client.post(
            "/auth/login",
            data={"username": username, "password": password},
            follow_redirects=follow_redirects
        )

    def logout(self, follow_redirects=True):
        return self._client.get("/auth/logout", follow_redirects=follow_redirects)

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.fixture(autouse=True)
def reset_id_counters():
    # reset id count to known condition just for Review and Favourite tests
    Review.id_count = 1
    Favourite.id_count = 1

    yield