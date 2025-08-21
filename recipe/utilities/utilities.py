import random

from flask import Blueprint, redirect
import recipe.adapters.repository as repo

utilities_bp = Blueprint('utilities_bp', __name__)

@utilities_bp.route('/utilities', methods=['GET'])
def get_random_recipe():
    random_recipe = repo.repo_instance.recipe_get_random()
    return redirect('/recipe/' + str(random_recipe.id))

def get_number_of_recipes():
    return repo.repo_instance.recipe_get_quantity()