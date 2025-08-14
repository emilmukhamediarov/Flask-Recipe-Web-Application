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
    def __init__(self, data_path: str):
        self._data_path = Path(data_path)

    def read_csv(self):
        if not self._data_path.exists():
            raise FileNotFoundError(f'{self._data_path} does not exist')

        with open(self._data_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                print(row)

reader = CSVDataReader("../data/recipes.csv")
reader.read_csv()