import random

from flask import Blueprint, render_template
import recipe.adapters.repository as repo

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    recipes = repo.repo_instance.recipe_get_all()
    number_of_recipes = len(recipes)
    random_recipe = random.choice(recipes)
    return render_template('home/home.html', recipe=random_recipe, number_of_recipes=number_of_recipes)