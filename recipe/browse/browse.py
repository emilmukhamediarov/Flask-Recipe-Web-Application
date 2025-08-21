import random
from math import ceil
from flask import Blueprint, render_template, request, abort, url_for, redirect
import recipe.adapters.repository as repo

from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.category import Category

# .recipe_get_all()
browse_bp = Blueprint('browse_bp', __name__)

PER_PAGE = 12

@browse_bp.route('/browse', methods=['GET'])
def browse():
    breadcrumbs = [
        ("Home", url_for("home_bp.home")),
        ("Browse", url_for("browse_bp.browse"))
    ]

    page = request.args.get('page', 1, type=int)
    list_of_recipes = repo.repo_instance.recipe_get_all()
    total = len(list_of_recipes)
    total_pages = ceil(total / PER_PAGE) if total else 1



    selected_category = request.args.get('category')
    all_categories = repo.repo_instance.category_get_all()
    print(all_categories[0].name)
    print(len(all_categories))
    print(all_categories)

    categories = {}
    for r in list_of_recipes:
        name = r.category.name if hasattr(r.category, 'name') else str(r.category)
        if not name:
            continue
        if name not in categories:
            categories[name] = Category(name)
        if r not in categories[name].recipes:
            categories[name].add_recipe(r)
    # for i in range(len(list_of_recipes)):
    #     recipe = list_of_recipes[i]
    #     categories[recipe.category] = i

    sorted_items = sorted(categories.items())
    num_categories = len(categories)



    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    page_recipes = list_of_recipes[start:end]

    window_start = max(1, page - 2)
    window_end = min(total_pages, page + 2)
    page_numbers = list(range(window_start, window_end + 1))

    show_first = 1 not in page_numbers
    show_last = total_pages not in page_numbers

    return render_template(
        '/browse/browse.html',
        recipes=page_recipes,
        page=page,
        total_pages=total_pages,
        page_numbers=page_numbers,
        show_first=show_first,
        show_last=show_last,
        categories=all_categories,
        selected_category=selected_category,

        num_categories=num_categories,

        breadcrumbs=breadcrumbs
    )