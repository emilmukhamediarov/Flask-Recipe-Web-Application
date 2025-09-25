from math import ceil
import pytest
import recipe.home.services as home_services
import recipe.browse.services as browse_services
import recipe.recipedetails.services as recipe_details_services
import recipe.favourites.services as favourite_services
import recipe.review.services as review_services
import recipe.auth.services as auth_services
import recipe.adapters.repository as repo
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.user import User
from datetime import date



# --- Home Services ---
def test_services_can_get_number_of_recipes(in_memory_repo):
    recipes = home_services.get_number_of_recipes(in_memory_repo)
    all_recipes = in_memory_repo.recipe_get_all()
    assert recipes == len(all_recipes)

def test_services_can_get_latest_recipes(in_memory_repo):
    latest = home_services.get_latest_recipes(in_memory_repo)
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

def test_services_can_get_review(in_memory_repo):
    user = User('RecipeTester987', 'RecipeTester987')
    author = Author(1, 'Maker')
    category = Category('Breakfast')
    recipe = Recipe(1, 'Carbohydrates', author, category=category)

    in_memory_repo.user_add(user)
    in_memory_repo.recipe_add(recipe)

    review_services.create_review(user.id, recipe.id, 3, "OK", date.today(), in_memory_repo)
    reviews = recipe_details_services.get_reviews(recipe.id, in_memory_repo)
    assert isinstance(reviews, list)
    assert len(reviews) == 1
    review_details = reviews[0]
    assert review_details["name"] == user.username
    assert review_details["rating"] == 3
    assert review_details["text"] == "OK"

def test_services_recipe_is_favourite(in_memory_repo):
    user = User('favouriteTest987', 'favouriteTest987')
    author = Author(1, 'Maker')
    category = Category('Breakfast')
    recipe = Recipe(1, 'Carbohydrates', author, category=category)

    in_memory_repo.user_add(user)
    in_memory_repo.recipe_add(recipe)

    assert recipe_details_services.recipe_is_favourite(user.id, recipe.id, in_memory_repo) is False

    favourite = Favourite(user.id, recipe.id)
    in_memory_repo.favourite_add(favourite)
    assert recipe_details_services.recipe_is_favourite(user.id, recipe.id, in_memory_repo) is True
    assert recipe_details_services.recipe_is_favourite(user.id, 9999, in_memory_repo) is False
    assert recipe_details_services.recipe_is_favourite(0, recipe.id, in_memory_repo) is False



# --- Favourites Services ---
def test_services_can_create_favourite(in_memory_repo):
    user = User("TestUser123", 'TestUser123')
    author = Author(1, 'John')
    category = Category('Milk')
    recipe = Recipe(1, 'CakePlaceholder', author, category=category)

    in_memory_repo.user_add(user)
    in_memory_repo.recipe_add(recipe)

    favourite_services.create_favourite(user.id, recipe.id, in_memory_repo)
    service_recipes = favourite_services.get_favourites(user.id, in_memory_repo)
    assert isinstance(service_recipes, list)
    assert len(service_recipes) == 1
    assert service_recipes[0] is recipe
    assert 'CakePlaceholder' in service_recipes[0].name


def test_services_can_remove_favourite(in_memory_repo):
    user = User("TestUser123", 'TestUser123')
    author = Author(1, 'John')
    category = Category('Milk')
    recipe = Recipe(1, 'CakePlaceholder', author, category=category)
    in_memory_repo.user_add(user)
    in_memory_repo.recipe_add(recipe)

    favourite_services.create_favourite(user.id, recipe.id, in_memory_repo)

    favourite_services.remove_favourite(user.id, recipe.id, in_memory_repo)
    service_recipes = favourite_services.get_favourites(user.id, in_memory_repo)
    assert isinstance(service_recipes, list)
    assert len(service_recipes) == 0
    assert favourite_services.get_favourites(user.id, in_memory_repo) == []

def test_services_can_get_favourites(in_memory_repo):
    user = User("TestUser123", 'TestUser123')
    author = Author(1, 'John')
    category = Category('Milk')
    r1 = Recipe(1, 'CakePlaceholder', author, category=category)
    r2 = Recipe(2, 'Toast', author, category=category)

    in_memory_repo.user_add(user)
    in_memory_repo.recipe_add(r1)
    in_memory_repo.recipe_add(r2)

    favourite_services.create_favourite(user.id, r1.id, in_memory_repo)
    favourite_services.create_favourite(user.id, r2.id, in_memory_repo)

    recipes = favourite_services.get_favourites(user.id, in_memory_repo)

    assert isinstance(recipes, list)
    assert len(recipes) == 2
    assert recipes[0] is r1
    assert recipes[1] is r2



# --- Review Services ---
def test_services_can_create_review(in_memory_repo):
    user = User("TestUser123", 'TestUser123')

    author = Author(1, 'John')
    category = Category('Dessert')
    recipe = Recipe(1, 'CakePlaceholder', author, category=category)

    in_memory_repo.user_add(user)
    in_memory_repo.recipe_add(recipe)

    review_services.create_review(user.id, recipe.id, 5, "Wow so good!", date.today(), in_memory_repo)

    reviews = in_memory_repo.reviews_get_all_by_recipe_id(recipe.id)
    assert isinstance(reviews, list)
    assert len(reviews) == 1
    r = reviews[0]
    assert r.user_id == user.id
    assert r.recipe_id == recipe.id
    assert r.rating == 5
    assert r.text == "Wow so good!"
    assert r.created_date == date.today()

def test_services_that_review_already_exists(in_memory_repo):
    user = User("TestUser123", "TestUser123")
    author = Author(1, 'John')
    category = Category('Dessert')
    recipe = Recipe(1, 'CakePlaceholder', author, category=category)
    recipe2 = Recipe(2, 'Toast', author, category=category)
    in_memory_repo.user_add(user)
    in_memory_repo.recipe_add(recipe)
    in_memory_repo.recipe_add(recipe2)

    review_services.create_review(user.id, recipe.id, 5, "Wow so good!", date.today(), in_memory_repo)

    review1_exists = review_services.review_already_exists(user.id, recipe.id, in_memory_repo)
    review2_nonexistent = review_services.review_already_exists(user.id, recipe2.id, in_memory_repo)
    assert review1_exists is True
    assert review2_nonexistent is False


# --- auth Services ---
def test_services_can_retrieve_user_by_name(in_memory_repo):
    user = User("authTester", 'authTester123')
    in_memory_repo.user_add(user)

    found_by_username = auth_services.retrieve_user_by_name("authTester", in_memory_repo)

    assert found_by_username == user
    assert found_by_username.username == "authTester"


def test_services_can_retrieve_user_by_id(in_memory_repo):
    user = User("authTester", 'authTester123')
    in_memory_repo.user_add(user)
    assert isinstance(user.id, int)

    found_by_id = auth_services.retrieve_user_by_id(user.id, in_memory_repo)

    assert found_by_id == user
    assert found_by_id.username == "authTester"


def test_services_can_add_new_user(in_memory_repo):
    new_user = User("NewUser123", 'NewUser123')

    auth_services.add_new_user(new_user, in_memory_repo)

    fetched = in_memory_repo.user_get_by_username("NewUser123")
    assert fetched is new_user
    assert new_user.id == fetched.id
    assert isinstance(new_user.id, int)

def test_services_retrieve_user_by_name_returns_none_when_name_nonexistent(in_memory_repo):
    assert auth_services.retrieve_user_by_name("does_not_exist_404", in_memory_repo) is None
