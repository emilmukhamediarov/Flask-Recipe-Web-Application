from flask import Blueprint, render_template
import recipe.adapters.repository as repo

recipe_details_bp = Blueprint('recipe_details_bp', __name__)

@recipe_details_bp.route('/recipe/<int:recipe_id>', methods=['GET'])

def get_recipe_details(recipe_id):
    get_recipe = repo.repo_instance.recipe_get_by_id(recipe_id)
    return render_template(
        'recipe_details/recipe_details.html',
        recipe = get_recipe
    )