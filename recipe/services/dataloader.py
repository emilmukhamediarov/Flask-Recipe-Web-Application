from recipe.adapters.datareader.csvdatareader import CSVDataReader
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.repository.authorrepo import AuthorRepo
from recipe.repository.reciperepo import RecipeRepo
from recipe.domainmodel.author import Author
from datetime import datetime
import re


reader = CSVDataReader()
rows = reader.read()

recipe_repo = RecipeRepo()
author_repo = AuthorRepo()

for row in rows:

    author = Author(author_id = int(row["AuthorId"]), name = row["AuthorName"])

    recipe = Recipe(recipe_id = int(row["RecipeId"]), name = row["Name"], author = author)
    recipe.cook_time = int(row["CookTime"])
    recipe.preparation_time = int(row["PrepTime"])

    date_str = row["DatePublished"]
    clean_date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
    recipe.date = datetime.strptime(clean_date_str, "%d %b %Y")

    recipe.description = row["Description"]
    recipe.images = [str(image) for image in row["Images"]]

    category = Category(name = row["RecipeCategory"])

    self.category =

    self.rating =
    self.nutrition =
    self.servings =
    self.recipe_yield =
    self.instructions =

    author.add_recipe(recipe)

    author_repo.add(author)
    recipe_repo.add(recipe)




