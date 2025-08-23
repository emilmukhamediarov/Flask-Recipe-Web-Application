import pytest
from datetime import date, datetime
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe

def test_repository_can_add_an_author(in_memory_repo):
    author = Author (1, 'John')
    in_memory_repo.author_add(author)
    assert in_memory_repo.author_get_by_name('John') is author

def test_repository_can_get_an_author_by_name(in_memory_repo):
    author = Author (1, 'John')
    in_memory_repo.author_add(author)
    assert in_memory_repo.author_get_by_name("John") is author

def test_repository_can_add_a_recipe(in_memory_repo):
    author = Author (1, 'John')
    category = Category( 'Milk')
    recipe = Recipe(1, 'Cake', author, category=category)
    in_memory_repo.recipe_add(recipe)
    assert in_memory_repo.recipe_get_by_name('Cake') is recipe

def test_repository_can_get_a_recipe_by_name(in_memory_repo):
    test_recipe = in_memory_repo.recipe_get_all()[10]
    retrieved_recipe = in_memory_repo.recipe_get_by_name(test_recipe.name)
    assert retrieved_recipe.name == test_recipe.name

def test_repository_can_get_all_recipies(in_memory_repo):
    recipies = in_memory_repo.recipe_get_all()
    assert len(recipies) > 1 and type(recipies) is list

def test_repository_can_add_a_category(in_memory_repo):
    category = Category('Milk')
    in_memory_repo.category_add(category)
    assert in_memory_repo.category_get_by_name('Milk') is category

def test_repository_can_get_a_category_by_name(in_memory_repo):
    category = Category('Test_category')
    in_memory_repo.category_add(category)
    assert in_memory_repo.category_get_by_name('Test_category') is category

def test_repository_can_add_a_category_by_name(in_memory_repo):
    in_memory_repo.category_add_by_name('Test_category')
    assert in_memory_repo.category_get_by_name('Test_category').name == 'Test_category'

def test_repository_can_get_all_categories(in_memory_repo):
    categories = in_memory_repo.category_get_all()
    assert len(categories) > 1 and type(categories) is list

def test_repository_can_get_a_list_of_category_names(in_memory_repo):
    category_names = in_memory_repo.category_get_all_names()
    assert len(category_names) > 1 and type(category_names) is list and type(category_names[0]) is str

def test_repository_can_get_recipes_by_category(in_memory_repo):
    category = Category('Fast good is not good for you')
    author = Author(1, 'John')
    one_recipe = Recipe(1, 'Fast food is delicious', author=author, category=category)
    two_recipe = Recipe(2, 'Another delicious fast food', author=author, category=category)
    in_memory_repo.recipe_add(one_recipe)
    in_memory_repo.recipe_add(two_recipe)
    recipes_by_category = in_memory_repo.recipes_get_all_by_category('Fast good is not good for you')
    assert len(recipes_by_category) == 2 and recipes_by_category[0] is one_recipe

def test_repository_can_get_recipes_by_id(in_memory_repo):
    author = Author (1, 'John')
    category = Category( 'Milk')
    recipe = Recipe(1, 'Cake', author, category=category)
    in_memory_repo.recipe_add(recipe)
    get_recipe_by_id = in_memory_repo.recipe_get_by_id(1)
    assert get_recipe_by_id is recipe

def test_repository_returns_number_of_recipies(in_memory_repo):
    length = in_memory_repo.recipe_get_quantity()
    assert type(length) is int

def test_repository_can_get_a_random_recipe(in_memory_repo):
    random_recipe_one = in_memory_repo.recipe_get_random()
    random_recipe_two = in_memory_repo.recipe_get_random()
    assert type(random_recipe_one) is Recipe and (not(random_recipe_one == random_recipe_two))

def test_repository_can_get_latest_recipe(in_memory_repo):
    latest_recipes = in_memory_repo.recipe_get_latest(5)
    assert len(latest_recipes) == 5

