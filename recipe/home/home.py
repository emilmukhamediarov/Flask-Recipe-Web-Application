import recipe.utilities.utilities as utilities
from flask import Blueprint, render_template, url_for
import recipe.adapters.repository as repo

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    breadcrumbs = [('Home', url_for('home_bp.home'))]
    number_of_recipes = utilities.get_number_of_recipes()
    latest_recipes = utilities.get_latest_recipes(4)
    return render_template('home/home.html', number_of_recipes=number_of_recipes, latest_recipes=latest_recipes, breadcrumbs=breadcrumbs)