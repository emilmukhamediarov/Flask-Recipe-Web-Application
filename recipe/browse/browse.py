import random
from math import ceil
from flask import Blueprint, render_template, request, url_for

from recipe.browse import services

browse_bp = Blueprint('browse_bp', __name__)

PER_PAGE = 12


@browse_bp.route('/browse', methods=['GET'])
def browse():
    breadcrumbs = [
        ("Home", url_for("home_bp.home")),
        ("Browse", url_for("browse_bp.browse"))
    ]

    # URl Parameters
    page = request.args.get('page', 1, type=int)
    selected_category = request.args.get('category')

    recipes = services.get_recipes()
    if selected_category:
        recipes = [recipe for recipe in recipes if recipe.category.name == selected_category]
        breadcrumbs.append((selected_category, url_for("browse_bp.browse", category=selected_category)))

    # Category Filters
    categories = services.get_categories()

    # Pagination
    page_recipes, total_pages, page_numbers, show_first, show_last = services.get_pagination(recipes, page)

    return render_template(
        '/browse/browse.html',
        page=page,
        selected_category=selected_category,
        categories=categories,

        recipes=page_recipes,
        total_pages=total_pages,
        page_numbers=page_numbers,
        show_first=show_first,
        show_last=show_last,

        breadcrumbs=breadcrumbs
    )