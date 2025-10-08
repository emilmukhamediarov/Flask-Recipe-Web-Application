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

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('recipe') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        # database_mode = False
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

        from .favourites import favourites
        app.register_blueprint(favourites.favourites_bp)

        from .review import review
        app.register_blueprint(review.review_bp)

    return app
