import random
from math import ceil
from flask import Blueprint, render_template, request, url_for
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
    selected_category = request.args.get('category')


    if selected_category:
        breadcrumbs.append((selected_category, url_for('browse_bp.category_view', category_name=selected_category)))

    all_recipes = repo.repo_instance.recipe_get_all()
    all_categories = repo.repo_instance.category_get_all()
    sorted_categories = sorted(all_categories, key=lambda c: c.name)

    filtered = []
    for r in all_recipes:
        if selected_category and (not r.category or r.category.name != selected_category):
            continue
        filtered.append(r)

    total = len(filtered)
    total_pages = ceil(total / PER_PAGE) if total else 1


    start = (page - 1) * PER_PAGE
    page_recipes = filtered[start:start + PER_PAGE]

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
        categories=sorted_categories,
        selected_category=selected_category,
        num_categories=len(all_categories),
        breadcrumbs=breadcrumbs,
        is_category_page=False,
        total_items=total
    )

@browse_bp.route('/category/<string:category_name>')
def category_view(category_name):
    page = request.args.get('page', 1, type=int)
    selected_category = request.args.get('category')
    breadcrumbs = [
        ("Home", url_for("home_bp.home")),
        ("Browse", url_for("browse_bp.browse")),
        (category_name, url_for('browse_bp.category_view', category_name=category_name))
    ]

    all_recipes = repo.repo_instance.recipe_get_all()
    all_categories = repo.repo_instance.category_get_all()
    sorted_categories = sorted(all_categories, key=lambda c: c.name)

    filtered = [r for r in all_recipes if r.category and r.category.name == category_name]


    total = len(filtered)
    total_pages = max(1, ceil(total / PER_PAGE))


    start = (page - 1) * PER_PAGE
    page_recipes = filtered[start:start + PER_PAGE]

    window_start = max(1, page - 2)
    window_end = min(total_pages, page + 2)
    page_numbers = list(range(window_start, window_end + 1))
    show_first = 1 not in page_numbers
    show_last = total_pages not in page_numbers
    print()
    return render_template(
        'browse/browse.html',
        recipes=page_recipes,
        page=page,
        total_pages=total_pages,
        page_numbers=page_numbers,
        show_first=show_first,
        show_last=show_last,
        categories=sorted_categories,
        selected_category=selected_category,
        num_categories=len(all_categories),
        breadcrumbs=breadcrumbs,
        is_category_page=True,
        total_items=total
    )