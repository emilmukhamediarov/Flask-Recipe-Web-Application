"""Initialize Flask app."""
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template

import recipe.adapters.repository as repo
from recipe.adapters.memory_repository import MemoryRepository, populate

from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author

def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    data_path = Path('recipe') / 'adapters' / 'data'

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_bp)

        from .recipedetails import recipedetails
        app.register_blueprint(recipedetails.recipe_details_bp)

        from .browse import browse
        app.register_blueprint(browse.browse_bp)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_bp)

    return app
