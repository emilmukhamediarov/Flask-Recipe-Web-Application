from datetime import datetime

from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.user import User



def test_db_repository_author_get_all_names(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    authors = repo.author_get_all_names()
    assert authors[0] == 'Troy A. Hakala'
    assert authors[1] == 'Carole Reu'
    assert authors[568] == 'Robbyn Snider'
    assert len(authors) == 569

def test_db_repository_category_get_all_names(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    categories = repo.category_get_all_names()
    assert categories[0] == 'Frozen Desserts'
    assert categories[1] == 'Beverages'
    assert len(categories) == 139

def test_db_repository_recipe_get_all(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipes = repo.recipe_get_all()
    assert isinstance(recipes[0], Recipe)
    assert isinstance(recipes[2454], Recipe)
    assert recipes[0].name == 'Low-Fat Berry Blue Frozen Dessert'

def test_db_repository_recipe_get_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    recipe = repo.recipe_get_by_id(38)
    assert isinstance(recipe, Recipe)
    assert recipe.name == 'Low-Fat Berry Blue Frozen Dessert'


def test_db_repository_recipe_get_quantity(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    quantity = repo.recipe_get_quantity()
    assert quantity == 2455

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
    assert latest[0].name == 'Pumpkin and Tomato Bake'
    assert latest[1].name == 'Tostones, or Fried Banana. (Venezuela)'
    assert latest[2].name == 'Pumpkin Eggnog Pie'
    assert latest[3].name == 'Sauteed Scallops with Mustard'


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
    assert repo.user_get_by_username("Username1234") == new_user
    assert repo.user_get_by_username("Username1234") != user_nonexistent

def test_db_repository_user_get_by_id(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user_nonexistent = repo.user_get_by_id("Username1234")
    assert user_nonexistent is None

    new_user = User("Username1234", "Password1234")
    assert repo.user_get_by_id(new_user.id) == new_user
    assert repo.user_get_by_id(user_nonexistent) != user_nonexistent