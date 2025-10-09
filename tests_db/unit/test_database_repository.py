from datetime import datetime

from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author



def test_repository_can_get_recipes(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    recipes = repo.get_all_recipes()
    assert len(recipes) == 13
