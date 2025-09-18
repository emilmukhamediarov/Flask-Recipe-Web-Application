import random
from math import ceil
from flask import Blueprint, render_template, request, url_for
import recipe.adapters.repository as repo

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
    selected_author = request.args.get('author')
    selected_sort = request.args.get('sort')
    search_term = request.args.get('search')



    recipes = services.get_recipes(repo.repo_instance)
    if selected_category:
        recipes = [recipe for recipe in recipes if recipe.category.name == selected_category]
        breadcrumbs.append((selected_category, url_for("browse_bp.browse", category=selected_category)))
    if selected_author:
        recipes = [recipe for recipe in recipes if recipe.author.name == selected_author]
        breadcrumbs.append((selected_author, url_for("browse_bp.browse", author=selected_author)))
    if search_term:
        recipes = [recipe for recipe in recipes if search_term.lower() in recipe.name.lower()]

    sorts = ["A-z", "Author", "Category"]

    if selected_sort == "A-z":
        recipes.sort(key=lambda recipe: recipe.name)
    elif selected_sort == "Author":
        recipes.sort(key=lambda recipe: recipe.author.name)
    elif selected_sort == "Category":
        recipes.sort(key=lambda recipe: recipe.category.name)
    else:
        recipes.sort()

    # Category Filters
    categories = services.get_categories(repo.repo_instance)

    # Author Filters
    authors = services.get_authors(repo.repo_instance)

    # Pagination
    page_recipes, total_pages, page_numbers, show_first, show_last = services.get_pagination(recipes, page)

    return render_template(
        '/browse/browse.html',
        page=page,
        selected_category=selected_category,
        selected_author=selected_author,
        selected_sort=selected_sort,
        search_term=search_term,

        categories=categories,
        authors=authors,
        sorts=sorts,

        recipes=page_recipes,
        total_pages=total_pages,
        page_numbers=page_numbers,
        show_first=show_first,
        show_last=show_last,

        breadcrumbs=breadcrumbs
    )