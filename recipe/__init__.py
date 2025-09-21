"""Initialize Flask app."""
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template

import recipe.adapters.repository as repo
from recipe.adapters.memory_repository import MemoryRepository, populate

from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('recipe') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

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

        from .auth import auth
        app.register_blueprint(auth.auth_bp)

        from recipe.favourites.favourites import favourites_bp
        app.register_blueprint(favourites_bp)

    return app
