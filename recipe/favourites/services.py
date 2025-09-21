from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.favourite import Favourite

class UserNotFound(Exception):
    pass

def create_favourite(user_id : int, recipe_id : int, repository : AbstractRepository):
    if repository.user_get_by_id(user_id) is None:
        raise UserNotFound
    f = Favourite(user_id, recipe_id)
    repository.favourite_add(f)

def remove_favourite(user_id : int, recipe_id : int, repository:AbstractRepository):
    if repository.user_get_by_id(user_id) is None:
        raise UserNotFound
    repository.favourite_remove(user_id, recipe_id)

def get_favourites(user_id: int, repository:AbstractRepository):
    return [repository.recipe_get_by_id(favourite.recipe_id) for favourite in repository.favourite_get_all_by_user_id(user_id)]

