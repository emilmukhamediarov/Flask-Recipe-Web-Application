import os
import csv
from pathlib import Path

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.review import Review

class CSVDataReader:
    def __init__(self, data_path):
        base_dir = Path(__file__).parent.parent.parent
        self._data_path = str(data_path / 'recipes.csv')

    def read(self):
        if not self._data_path:
            raise FileNotFoundError(f'{self._data_path} does not exist')

        with open(self._data_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            return list(reader)