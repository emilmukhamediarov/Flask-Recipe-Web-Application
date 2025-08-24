import pytest

from recipe.adapters.memory_repository import MemoryRepository, populate

from utils import get_project_root

TEST_DATA_PATH = get_project_root() / "tests" / "data"

@pytest.fixture
def in_memory_repo():
    test_repo = MemoryRepository()
    populate(TEST_DATA_PATH, test_repo)
    return test_repo

