import recipe.adapters.repository as repo
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.memory_repository import MemoryRepository

def get_recipe(id : int, repository:AbstractRepository):
    return repository.recipe_get_by_id(id)