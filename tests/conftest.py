import pytest

from recipe import create_app
from recipe.adapters import memory_repository
from recipe.adapters.memory_repository import MemoryRepository
from recipe.adapters.datareader.csv_data_reader import CSVDataReader

@pytest.fixture
def in_memory_repo():
    test_reader = CSVDataReader()
    test_data = test_reader.read()
    test_repo = MemoryRepository()
    test_repo.populate(test_data)
    return test_repo

