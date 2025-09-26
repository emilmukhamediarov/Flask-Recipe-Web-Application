from flask import Blueprint, render_template, url_for, session
import recipe.adapters.repository as repo
import recipe.recipedetails.services as services

recipe_details_bp = Blueprint('recipe_details_bp', __name__)

@recipe_details_bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):

    recipe = services.get_recipe(recipe_id, repo.repo_instance)
    reviews = services.get_reviews(recipe, repo.repo_instance)

    is_favourite = services.recipe_is_favourite(session.get('user_id'), recipe_id, repo.repo_instance)

    breadcrumbs = [
        ("Home", url_for("home_bp.home")),
        ("Browse", url_for("browse_bp.browse")),
        (recipe.category.name, url_for("browse_bp.browse", category=recipe.category.name)),
        (recipe.name, url_for("recipe_details_bp.get_recipe_details", recipe_id=recipe.id)),
    ]
    return render_template(
        'recipe_details/recipe_details.html',
        recipe = recipe, breadcrumbs = breadcrumbs, reviews = reviews, is_favourite = is_favourite
    )