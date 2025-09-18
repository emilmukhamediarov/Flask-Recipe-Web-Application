import pytest

from recipe import create_app
from recipe.adapters.memory_repository import MemoryRepository, populate

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
        self.__client = client

    def login(self, user_name='username', password='password'):
        return self.__client.post(
            'authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
