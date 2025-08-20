import pytest
from datetime import date, datetime
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe

def test_repository_can_add_an_author(in_memory_repo):
    author = Author (1, 'John')
    in_memory_repo.author_add(author)

    assert in_memory_repo.author_get_all()[0] is author