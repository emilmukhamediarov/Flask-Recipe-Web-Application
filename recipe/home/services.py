import recipe.adapters.repository as repo
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.memory_repository import MemoryRepository

NUMBER_OF_FEATURE_RECIPES = 4

def get_number_of_recipes(repository:AbstractRepository):
    return repository.recipe_get_quantity()

def get_latest_recipes(repository:AbstractRepository):
    return repository.recipe_get_latest(NUMBER_OF_FEATURE_RECIPES)