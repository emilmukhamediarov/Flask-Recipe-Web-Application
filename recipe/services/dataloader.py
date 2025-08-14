from recipe.adapters.datareader.csvdatareader import CSVDataReader
from recipe.domainmodel.recipe import Recipe
from recipe.repository.reciperepository import RecipeRepository

reader = CSVDataReader()
rows = reader.read()

recipe_repo = RecipeRepository()

for row in rows:
    