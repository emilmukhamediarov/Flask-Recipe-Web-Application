from flask import Blueprint, render_template, url_for
import recipe.adapters.repository as repo

import recipe.home.services as services

home_bp = Blueprint('home_bp', __name__)

@home_bp.route('/', methods=['GET'])
def home():
    breadcrumbs = [('Home', url_for('home_bp.home'))]
    number_of_recipes = services.get_number_of_recipes(repo.repo_instance)
    latest_recipes = services.get_latest_recipes(repo.repo_instance)
    return render_template('home/home.html', number_of_recipes=number_of_recipes, latest_recipes=latest_recipes, breadcrumbs=breadcrumbs)