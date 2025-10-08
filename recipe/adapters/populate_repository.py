import os
from pathlib import Path

from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.csv_data_reader import CSVDataReader


def populate(data_path: Path, repo: AbstractRepository):
    reader = CSVDataReader(data_path)

    # # Get the absolute path to the data directory
    # dir_name = os.path.abspath(data_path)
    #
    # recipe_filename = os.path.join(dir_name, "recipes.csv")

    reader.read()

    authors = reader.authors
    recipes = reader.recipes
    categories = reader.categories

    repo.add_multiple_authors(authors)
    repo.add_multiple_recipes(recipes)
    repo.add_multiple_categories(categories)
