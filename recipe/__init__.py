"""Initialize Flask app."""
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from recipe.adapters.database_repository import SqlAlchemyRepository
from recipe.adapters.orm import mapper_registry, map_model_to_tables
from sqlalchemy.pool import NullPool

from flask import Flask, render_template

import recipe.adapters.repository as repo

from recipe.adapters.memory_repository import MemoryRepository
from recipe.adapters.populate_repository import populate
from recipe.adapters import memory_repository, repository

from recipe.adapters import memory_repository, repository

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

    elif app.config['REPOSITORY'] == 'database':

        database_uri = 'sqlite:///recipes.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

        # STEP 2: Create a database engine and connect it to the specified database
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False},
                                        poolclass=NullPool,
                                        echo=False)

        # STEP 3: Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True,
                                       bind=database_engine)

        # STEP 4: Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = SqlAlchemyRepository(session_factory)
        data_path = Path('recipe') / 'adapters' / 'data'

        # STEP 4: Repopulate the DB.
        if len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            # Conditionally create database tables.
            mapper_registry.metadata.create_all(database_engine)
            # Remove any data from the tables.
            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            repo.repo_instance = SqlAlchemyRepository(session_factory)
            populate(data_path, repo.repo_instance)

            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()


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
