from flask import Blueprint, render_template
import recipe.adapters.repository as repo

recipedetails_bp = Blueprint('recipedetails_bp', __name__)

@recipedetails_bp.route('/recipe', methods=['GET'])

def get_recipe_details():
    get_recipe = repo.repo_instance.recipe_get_all()[0]
    return render_template(
        'recipes/recipedetails.html',
        recipe = get_recipe
    )