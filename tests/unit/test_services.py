from math import ceil
import pytest
import recipe.home.services as home_services
import recipe.browse.services as browse_services
import recipe.adapters.repository as repo
from recipe.domainmodel.category import Category
# --- Home Services ---
def test_services_can_get_number_of_recipes(in_memory_repo):
    recipes = in_memory_repo.recipe_get_quantity()
    assert recipes == 2455

def test_services_can_get_latest_recipes(in_memory_repo):
    latest = in_memory_repo.recipe_get_latest(home_services.NUMBER_OF_FEATURE_RECIPES)
    assert len(latest) == home_services.NUMBER_OF_FEATURE_RECIPES



# --- Browse Services ---
def test_services_can_get_recipes(in_memory_repo):
    repo.repo_instance = in_memory_repo
    repo_list = in_memory_repo.recipe_get_all()
    service_list = browse_services.get_recipes()

    assert isinstance(service_list, list)
    assert len(service_list) == len(repo_list)
    assert [r.id for r in service_list] == [r.id for r in repo_list]

