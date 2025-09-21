from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.favourite import Favourite

def add_new_favourite(new_favourite:Favourite, repository:AbstractRepository):
        repository.favourite_add(new_favourite)

def remove_favourite(favourite: Favourite, repository:AbstractRepository):
        repository.favourite_remove(favourite)

def get_favourites(user_id: int, repository:AbstractRepository):
    return [repository.recipe_get_by_id(favourite.recipe_id) for favourite in repository.favourite_get_all_by_user_id(user_id)]

