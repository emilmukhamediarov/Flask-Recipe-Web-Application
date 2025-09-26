from recipe.adapters.repository import AbstractRepository

def get_recipe(id : int, repository:AbstractRepository):
    return repository.recipe_get_by_id(id)

def get_reviews(id : int, repository:AbstractRepository):
    return [{
        'name': repository.user_get_by_id(review.user_id).username,
        'rating': review.rating,
        'text': review.text,
        'created_date': review.created_date
    } for review in repository.reviews_get_all_by_recipe_id(id)].sort(key=lambda review: review['created_date'], reverse=True) #Displays reviews with newest first

def recipe_is_favourite(user_id, recipe_id, repository:AbstractRepository):
    if not user_id:
        return False
    return len([f for f in repository.favourite_get_all_by_user_id(user_id) if f.recipe_id == recipe_id]) > 0
