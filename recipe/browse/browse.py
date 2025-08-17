import random

from flask import Blueprint, render_template
import recipe.adapters.repository as repo

from recipe.adapters.repository import AbstractRepository
# .recipe_get_all()
browse_bp = Blueprint('browse_bp', __name__)

@browse_bp.route('/browse', methods=['GET'])
def browse():
    recipes = repo.repo_instance.recipe_get_all()
    number_of_recipes = len(recipes)
    random_0 = recipes[0]
    random_recipe = random.choice(recipes)
    return render_template('samples/browse.html', recipe=random_0, number_of_recipes=number_of_recipes, random_recipe=random_recipe)