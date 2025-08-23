import pytest

from recipe import create_app
from recipe.adapters import memory_repository
from recipe.adapters.memory_repository import MemoryRepository
from recipe.adapters.datareader.csv_data_reader import CSVDataReader
from pathlib import Path

test_data_path = Path('tests') / 'data'

@pytest.fixture
def in_memory_repo():
    test_repo = MemoryRepository()
    memory_repository.populate(test_data_path, test_repo)
    return test_repo

