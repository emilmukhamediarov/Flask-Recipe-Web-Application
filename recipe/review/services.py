from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.review import Review

class UserNotFound(Exception):
    pass

def create_review(user_id, recipe_id, rating, text, created_date, repository : AbstractRepository):
    if not repository.user_get_by_id(user_id):
        raise UserNotFound
    r = Review(user_id, recipe_id, rating, text, created_date)
    recipe = repository.recipe_get_by_id(recipe_id)
    recipe.add_review(r)
    repository.reviews_add(r)

def delete_review(review_id : int, repository : AbstractRepository):
    review = repository.reviews_get_by_id(review_id)
    recipe_id = review.recipe_id
    recipe = repository.recipe_get_by_id(recipe_id)
    recipe.remove_review(review)
    repository.reviews_remove(review)

def review_already_exists(user_id, recipe_id, repository : AbstractRepository):
    reviews = repository.reviews_get_all_by_recipe_id(recipe_id)
    for review in reviews:
        if review.user_id == user_id:
            return True
    return False