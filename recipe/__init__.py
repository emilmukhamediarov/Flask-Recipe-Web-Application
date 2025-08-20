"""Initialize Flask app."""
from datetime import datetime
from flask import Flask, render_template

import recipe.adapters.repository as repo
from recipe.adapters.memory_repository import MemoryRepository

from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author

def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    repo.repo_instance = MemoryRepository()
    repo.repo_instance.populate()
    list_of_recipes = repo.repo_instance.recipe_get_all()

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_bp)


        from .recipedetails import recipedetails
        app.register_blueprint(recipedetails.recipedetails_bp)

        from .browse import browse
        app.register_blueprint(browse.browse_bp)

# might break remove if does
    @app.route('/recipe_detail')
    def recipe_detail():  # put application's code here
        return render_template('samples/recipe_detail.html')

    @app.route('/recipe/<int:recipe_id>')
    def recipe(recipe_id):  # put application's code here
        # recipe = next(recipe for recipe in list_of_recipes if recipe.id == recipe.id)
        recipe_obj = next((r for r in list_of_recipes if r.id == recipe_id))
        return render_template('samples/recipe_detail.html', recipe=recipe_obj)
# conflict?
    return app
