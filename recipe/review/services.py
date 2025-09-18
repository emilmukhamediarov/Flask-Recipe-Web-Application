from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.review import Review


def add_review(review : Review, repository:AbstractRepository):
    repository.reviews_add(review)