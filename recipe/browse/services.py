from math import ceil
from typing import TYPE_CHECKING, List
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.memory_repository import MemoryRepository

if TYPE_CHECKING:
    from recipe.domainmodel.recipe import Recipe

import recipe.adapters.repository as repo

PER_PAGE = 12

def get_recipes(repository:AbstractRepository):
    return repository.recipe_get_all()

def get_categories(repository:AbstractRepository):
    return sorted(repository.category_get_all_names())

def get_authors(repository:AbstractRepository):
    return sorted(repository.author_get_all_names())

def get_pagination(recipes : List["Recipe"], page : int):
    number_of_recipes = len(recipes)
    total_pages = ceil(number_of_recipes / PER_PAGE)

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_recipes = recipes[start:end]

    window_start = max(1, page - 2)
    window_end = min(total_pages, page + 2)
    page_numbers = list(range(window_start, window_end + 1))

    show_first = 1 not in page_numbers
    show_last = total_pages not in page_numbers

    return page_recipes, total_pages, page_numbers, show_first, show_last
