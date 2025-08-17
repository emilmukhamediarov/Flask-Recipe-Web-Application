from flask import Blueprint, render_template

recipedetails_bp = Blueprint('recipedetails_bp', __name__)

@recipedetails_bp.route('/recipe', methods=['GET'])
def get_recipe_details():
    return render_template('recipes/recipedetail.html')

def home():
    return render_template(
        'home/home.html',
        selected_articles=utilities.get_selected_articles(),
        tag_urls=utilities.get_tags_and_urls()
    )