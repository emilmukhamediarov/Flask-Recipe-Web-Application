import pytest

from recipe import create_app
from recipe.adapters import memory_repository
from recipe.adapters.memory_repository import MemoryRepository

@pytest.fixture
def in_memory_repo():
    test_repo = MemoryRepository()
    test_repo.populate()
    return test_repo

