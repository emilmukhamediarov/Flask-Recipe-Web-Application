from datetime import datetime

from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.domainmodel.favourite import Favourite



def test_db_repository_author_get_all_names(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    authors = repo.author_get_all_names()
    assert authors[0] == 'Carole Reu'
    assert authors[1] == 'Mimi Hiller'
    assert authors[35] == 'bugsbunnyfan'
    assert len(authors) == 36

def test_db_repository_category_get_all_names(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    categories = repo.category_get_all_names()
    assert categories[0] == 'Frozen Desserts'
    assert categories[1] == 'Beverages'
    assert len(categories) == 27

def test_db_repository_recipe_get_all(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipes = repo.recipe_get_all()
    assert isinstance(recipes[0], Recipe)
    assert isinstance(recipes[49], Recipe)
    assert recipes[0].name == 'Low-Fat Berry Blue Frozen Dessert'

def test_db_repository_recipe_get_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe = repo.recipe_get_by_id(38)
    assert isinstance(recipe, Recipe)
    assert recipe.name == 'Low-Fat Berry Blue Frozen Dessert'


def test_db_repository_recipe_get_quantity(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    quantity = repo.recipe_get_quantity()
    assert quantity == 50

def test_db_repository_recipe_get_random(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    random = repo.recipe_get_random()
    assert isinstance(random, Recipe)

    random2 = repo.recipe_get_random()
    assert isinstance(random2, Recipe)

    assert random != random2

def test_db_repository_recipe_get_latest(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    latest = repo.recipe_get_latest(4)
    assert isinstance(latest, list)
    assert len(latest) == 4
    assert latest[0].name == 'Chocolate Cream Meringue Pie'
    assert latest[1].name == 'Chocolate Pudding II'
    assert latest[2].name == 'Chocolate Coffee'
    assert latest[3].name == 'Chocolate Pudding'


def test_db_repository_user_add(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user = User("Username1234", "Password1234")
    repo.user_add(user)

    assert repo.user_get_by_username("Username1234") == user

def test_db_repository_user_get_by_username(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user_nonexistent = repo.user_get_by_username("Username1234")
    assert user_nonexistent is None

    new_user = User("Username1234", "Password1234")
    repo.user_add(new_user)
    assert repo.user_get_by_username("Username1234") == new_user


def test_db_repository_user_get_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user_nonexistent = repo.user_get_by_id(99999)
    assert user_nonexistent is None

    new_user = User("Username1234", "Password1234")
    repo.user_add(new_user)
    assert repo.user_get_by_id(new_user.id) == new_user


def test_db_repository_reviews_add(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    review = Review(1, 38, 4, "Amazing", datetime.today())

    repo.reviews_add(review)

    test = repo.reviews_get_by_id(1)

    assert isinstance(test, Review)
    assert test.user_id == 1
    assert test.recipe_id == 38
    assert test.rating == 4
    assert test.text == "Amazing"

def test_db_repository_reviews_remove(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    review = Review(1, 38, 4, "Amazing", datetime.today())

    repo.reviews_add(review)

    test = repo.reviews_get_by_id(review.id)
    assert isinstance(test, Review)

    repo.reviews_remove(review)

    removed_recipe = repo.reviews_get_by_id(review.id)
    assert removed_recipe is None

def test_db_repository_reviews_get_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    no_review = repo.reviews_get_by_id(9999)
    assert no_review is None

    review = Review(1, 38, 4, "Amazing", datetime.today())
    repo.reviews_add(review)
    test = repo.reviews_get_by_id(review.id)
    assert isinstance(test, Review)
    assert test.user_id == 1
    assert test.recipe_id == 38
    assert test.rating == 4
    assert test.text == "Amazing"

def test_db_repository_reviews_get_all_by_user_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    review1 = Review(1, 38, 4, "Frozen", datetime.today())
    review2 = Review(1, 40, 4, "Amazing", datetime.today())
    review3 = Review(2, 38, 4, "Test case", datetime.today())

    repo.reviews_add(review1)
    repo.reviews_add(review2)
    repo.reviews_add(review3)

    reviews_by_user_1 = repo.reviews_get_all_by_user_id(1)
    assert isinstance(reviews_by_user_1, list)
    assert len(reviews_by_user_1) == 2
    assert reviews_by_user_1[0] == review1
    assert reviews_by_user_1[1] == review2

    reviews_by_user_2 = repo.reviews_get_all_by_user_id(2)
    assert isinstance(reviews_by_user_2, list)
    assert len(reviews_by_user_2) == 1
    assert reviews_by_user_2[0] == review3

def test_db_repository_reviews_get_all_by_recipe_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    review1 = Review(1, 38, 4, "Frozen", datetime.today())
    review2 = Review(1, 40, 4, "Amazing", datetime.today())
    review3 = Review(3, 38, 4, "Test case", datetime.today())

    repo.reviews_add(review1)
    repo.reviews_add(review2)
    repo.reviews_add(review3)
    reviews_by_recipe_38 = repo.reviews_get_all_by_recipe_id(38)
    assert isinstance(reviews_by_recipe_38, list)
    assert len(reviews_by_recipe_38) == 2
    assert reviews_by_recipe_38[0] == review1
    assert reviews_by_recipe_38[1] == review3

    reviews_by_recipe_40 = repo.reviews_get_all_by_recipe_id(40)
    assert isinstance(reviews_by_recipe_40, list)
    assert len(reviews_by_recipe_40) == 1
    assert reviews_by_recipe_40[0] == review2

def test_db_repository_favourite_add(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    favourite = Favourite(1, 38)

    repo.favourite_add(favourite)

    all_favourites = repo.favourite_get_all_by_user_id(1)
    assert isinstance(all_favourites, list)
    assert len(all_favourites) == 1
    assert all_favourites[0] == favourite

def test_db_repository_favourite_get_all_by_user_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    favourite = Favourite(1, 38)
    favourite1 = Favourite(2, 38)
    favourite2 = Favourite(2, 40)

    repo.favourite_add(favourite)
    repo.favourite_add(favourite1)
    repo.favourite_add(favourite2)

    all_favourites_user_1 = repo.favourite_get_all_by_user_id(1)
    assert isinstance(all_favourites_user_1, list)
    assert len(all_favourites_user_1) == 1
    assert all_favourites_user_1[0].recipe_id == 38

    all_favourites_user_2 = repo.favourite_get_all_by_user_id(2)
    assert isinstance(all_favourites_user_2, list)
    assert len(all_favourites_user_2) == 2
    assert all_favourites_user_2[0].recipe_id == 38
    assert all_favourites_user_2[1].recipe_id == 40
