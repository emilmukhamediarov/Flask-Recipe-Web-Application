from math import ceil
import pytest
import recipe.home.services as home_services
import recipe.browse.services as browse_services
import recipe.recipedetails.services as recipe_details_services
import recipe.adapters.repository as repo
from recipe.domainmodel.category import Category

# --- Home Services ---
def test_services_can_get_number_of_recipes(in_memory_repo):
    recipes = home_services.get_number_of_recipes(in_memory_repo)
    all_recipes = in_memory_repo.recipe_get_all()
    assert recipes == len(all_recipes)

def test_services_can_get_latest_recipes(in_memory_repo):
    latest = in_memory_repo.recipe_get_latest(home_services.NUMBER_OF_FEATURE_RECIPES)
    assert len(latest) == home_services.NUMBER_OF_FEATURE_RECIPES



# --- Browse Services ---
def test_services_can_get_recipes(in_memory_repo):
    repo_list = in_memory_repo.recipe_get_all()
    service_list = browse_services.get_recipes(in_memory_repo)

    assert isinstance(service_list, list)
    assert len(service_list) == len(repo_list)
    assert [r.id for r in service_list] == [r.id for r in repo_list]


def test_services_can_get_categories(in_memory_repo):
    repo_list = in_memory_repo.category_get_all_names()
    service_list = browse_services.get_categories(in_memory_repo)
    expected = sorted(repo_list)

    assert isinstance(service_list, list)
    assert service_list == expected
    assert service_list == sorted(service_list)

def test_services_can_get_authors(in_memory_repo):
    repo_list = in_memory_repo.author_get_all_names()
    service_list = browse_services.get_authors(in_memory_repo)
    expected = sorted(repo_list)

    assert isinstance(service_list, list)
    assert service_list == expected
    assert service_list == sorted(service_list)

def test_services_can_get_pagination(in_memory_repo):
    all_recipes = in_memory_repo.recipe_get_all()
    total = len(all_recipes)
    page = 1
    page_recipes, total_pages, page_numbers, show_first, show_last = browse_services.get_pagination(all_recipes, page=page)

    assert total_pages == ceil(total / browse_services.PER_PAGE) if total else 0
    assert len(page_recipes) == min(browse_services.PER_PAGE, total)
    if total_pages >= 1:
        assert 1 in page_numbers
    assert isinstance(page_recipes, list)
    assert page_numbers == [1, 2, 3]
    assert show_first == (1 not in page_numbers)
    assert show_last == (total_pages not in page_numbers)


# --- RecipeDetails Services ---
def test_services_can_get_recipe(in_memory_repo):
    repo_list = in_memory_repo.recipe_get_all()
    first = repo_list[0]
    returned = recipe_details_services.get_recipe(first.id, in_memory_repo)
    assert len(repo_list) > 0
    assert returned is not None
    assert returned.id == first.id