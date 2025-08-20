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


    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_bp)


        from .recipedetails import recipedetails
        app.register_blueprint(recipedetails.recipe_details_bp)

        from .browse import browse
        app.register_blueprint(browse.browse_bp)


    return app
