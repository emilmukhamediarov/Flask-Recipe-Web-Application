from flask import Blueprint, render_template, url_for
import recipe.adapters.repository as repo

recipe_details_bp = Blueprint('recipe_details_bp', __name__)

@recipe_details_bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def get_recipe_details(recipe_id):

    get_recipe = repo.repo_instance.recipe_get_by_id(recipe_id)
    breadcrumbs = [
        ("Home", url_for("home_bp.home")),
        ("Browse", url_for("browse_bp.browse")),
        (get_recipe.category.name, url_for("browse_bp.browse", category=get_recipe.category.name)),
        (get_recipe.name, url_for("recipe_details_bp.get_recipe_details", recipe_id=get_recipe.id)),

    ]
    return render_template(
        'recipe_details/recipe_details.html',
        recipe = get_recipe, breadcrumbs = breadcrumbs,
    )