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
    # recipes = repo.repo_instance.recipe_get_all()
    # number_of_recipes = len(recipes)
    # random_0 = recipes[0]
    # random_recipe = random.choice(recipes)
    # return render_template('samples/browse.html', recipes=recipes, recipe=random_0, number_of_recipes=number_of_recipes, random_recipe=random_recipe)

    # page number from query string, default 1
    page = request.args.get('page', 1, type=int)
    list_of_recipes = repo.repo_instance.recipe_get_all()
    total = len(list_of_recipes)
    total_pages = ceil(total / PER_PAGE) if total else 1


    selected_category = request.args.get('category')

    # categories = {}
    # for r in list_of_recipes:
    #     name = r.category
    #     categories.setdefault(name.name)
    #     if r not in name.recipes:
    #         name.add_recipe(r)

    categories = repo.repo_instance.category_get_all()

    sorted_items = sorted([c.name for c in categories])
    num_categories = len(categories)



    # guard dont need: if page out of range, redirect to page 1 (or abort(404))
    # if page < 1 or page > total_pages:
    #     return redirect(url_for('browse', page=1))

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
        categories=sorted_items,
        selected_category=selected_category,

        num_categories=num_categories,

        breadcrumbs=breadcrumbs
    )