import recipe.adapters.repository as repo
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.memory_repository import MemoryRepository

def get_recipe(id : int, repository:AbstractRepository):
    return repository.recipe_get_by_id(id)

def get_reviews(id : int, repository:AbstractRepository):
    return [{
        'name': repository.user_get_by_id(review.user_id).username,
        'rating': review.rating,
        'text': review.text
    } for review in repository.reviews_get_all_by_recipe_id(id)]
