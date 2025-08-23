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


