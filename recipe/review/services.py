from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.review import Review

class UserNotFound(Exception):
    pass

def create_review(user_id, recipe_id, rating, text, repository : AbstractRepository):
    if not repository.user_get_by_id(user_id):
        raise UserNotFound
    r = Review(user_id, recipe_id, rating, text)
    repository.reviews_add(r)