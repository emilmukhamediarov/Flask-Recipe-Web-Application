from abc import ABC
from typing import List, Type

from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.exc import NoResultFound

from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction

# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self) -> object:
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def author_add(self, author) -> None:
        """Adds an Author to the repository"""
        pass

    def author_get_by_name(self, author_name) -> Author:
        """Returns an Author by their name"""
        pass

    def author_get_all(self) -> List[Author]:
        """Returns a list of Authors"""
        pass

    def author_get_all_names(self) -> List[Author]:
        """Returns a list of Author names"""
        pass

    def category_add(self, category) -> None:
        """Adds a Category to the repository"""
        pass

    def category_get_by_name(self, category_name) -> Category:
        """Returns a Category by its name"""
        pass

    def category_add_by_name(self, category_name) -> Category:
        """Creates a new Category with the given name and returns the new object"""
        pass

    def category_get_all(self) -> List[Category]:
        """Returns a list of Categories"""
        pass

    def category_get_all_names(self) -> List[str]:
        """Returns a list of Category Names"""
        pass

    def recipe_add(self, recipe) -> None:
        """Adds a Recipe to the repository"""
        pass

    def recipe_get_by_name(self, recipe_name) -> Recipe:
        """Returns a Recipe by its name"""
        pass

    def recipe_get_all(self) -> List[Recipe]:
        """Returns a list of Recipes"""
        pass

    def recipes_get_all_by_category(self, category_name) -> List[Recipe]:
        """Returns a list of Recipes by category"""
        pass

    def recipe_get_by_id(self, recipe_id) -> Recipe:
        """Returns a Recipe by its id"""
        pass

    def recipe_get_quantity(self) -> int:
        return self._session_cm.session.query(Recipe).count()

    def recipe_get_random(self) -> Recipe:
        """Returns a random Recipe"""
        pass

    def recipe_get_latest(self, num: int):
        return self._session_cm.session.query(Recipe).order_by(Recipe._Recipe__id.desc()).limit(num).all()

    def user_add(self, user: User):
        """Adds User to the dictionary"""
        pass

    def user_get_by_username(self, username: str) -> User:
        """Returns the User by username"""
        pass

    def user_get_by_id(self, user_id: int) -> User:
        """Returns the User by id"""
        pass

    def reviews_add(self, review) -> None:
        pass

    def reviews_remove(self, review) -> None:
        pass

    def reviews_get_by_id(self, review_id: int) -> Review:
        pass

    def reviews_get_all_by_user_id(self, user_id: int) -> List[Review]:
        pass

    def reviews_get_all_by_recipe_id(self, recipe_id: int) -> List[Review]:
        pass

    def favourite_add(self, recipe) -> None:
        """Adds a recipe to favourites"""
        pass

    def favourite_remove(self, user_id, recipe_id) -> None:
        """Removes a favourite by id match"""
        pass

    def favourite_get_all(self) -> List[Favourite]:
        """Returns a list of favourites"""
        pass

    def favourite_get_all_by_user_id(self, user_id) -> List[Favourite]:
        """Returns a list of favourites by user_id"""
        pass
    #
    # # region User_data Methods to manage Users
    # def add_user(self, user: User):
    #     pass
    #
    # def get_user(self, username: str) -> User:
    #     pass
    #
    # # endregion
    #
    # # region Author_data Methods to manage Authors
    # def add_author(self, author: Author):
    #     with self._session_cm as scm:
    #         with scm.session.no_autoflush:
    #             # Check if author already exists
    #             existing_author = scm.session.query(Author).filter(Author.id == author.id).first()
    #             if not existing_author:
    #                 scm.session.add(author)
    #         scm.commit()
    #
    # def get_authors(self) -> List[Author]:
    #     authors = self._session_cm.session.query(Author).all()
    #     return authors
    #
    # def get_authors(self, sort_method: str) -> List[Author]:
    #     authors = self._session_cm.session.query(Author).all()
    #     return authors
    #
    # def get_number_of_authors(self) -> int:
    #     num_authors = self._session_cm.session.query(Author).count()
    #     return num_authors
    #
    # def add_multiple_authors(self, authors: List[Author]):
    #     with self._session_cm as scm:
    #         with scm.session.no_autoflush:
    #             for author in authors:
    #                 # Check if author already exists
    #                 existing_author = scm.session.query(Author).filter(Author.id == author.id).first()
    #                 if not existing_author:
    #                     scm.session.add(author)
    #         scm.commit()
    #
    # # endregion
    #
    # # region Category_data Methods to manage Categories
    # def add_category(self, category: Category):
    #     pass
    #
    # def get_category_by_name(self, name: str) -> Category:
    #     pass
    #
    # def get_categories(self) -> List[Category]:
    #     pass
    #
    # def get_number_of_categories(self) -> int:
    #     pass
    #
    # def add_multiple_categories(self, categories: List[Category]):
    #     pass
    #
    # # endregion
    #
    # # region Recipe_data Methods to manage Recipes
    #
    # def add_recipe(self, recipe: Recipe):
    #     pass
    #


    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
                    scm.session.add(recipe)
            scm.commit()

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    scm.session.add(author)
            scm.commit()

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()


    # def get_recipe(self, recipe_id: int) -> Recipe:
    #     recipe = None
    #     try:
    #         query = self._session_cm.session.query(Recipe).filter(
    #             Recipe._Recipe__id == recipe_id)
    #         recipe = query.one()
    #         # Populate the recipe with related data for consistent domain model interface
    #         self._populate_recipe_data(recipe)
    #     except NoResultFound:
    #         print(f'Recipe {recipe_id} was not found')
    #
    #     return recipe
    #
    # def get_recipes(self, page: int, page_size: int, sort_method: str) -> List[Recipe]:
    #     query = self._session_cm.session.query(Recipe)
    #
    #     # Apply pagination
    #     start_index = (page - 1) * page_size
    #     recipes = query.offset(start_index).limit(page_size).all()
    #
    #     # Populate all recipes with related data
    #     for recipe in recipes:
    #         self._populate_recipe_data(recipe)
    #
    #     return recipes
    #
    # def get_all_recipes(self, sort_method: str = 'name') -> List[Recipe]:
    #     query = self._session_cm.session.query(Recipe)
    #
    #     recipes = query.all()
    #     # Populate all recipes with related data
    #     for recipe in recipes:
    #         self._populate_recipe_data(recipe)
    #     return recipes
    #
    # def get_recipes_with_category_filter(self, page: int, page_size: int, sort_method: str,
    #                                      category_name: str = None) -> tuple[List[Recipe], int]:
    #     pass
    #
    # def search_recipes(self, search_type: str, search_term: str, page: int, page_size: int, sort_method: str,
    #                    category_name: str = None) -> tuple[List[Recipe], int]:
    #     pass
    #
    # def get_number_of_recipes(self) -> int:
    #     num_recipes = self._session_cm.session.query(Recipe).count()
    #     return num_recipes
    #
    # def get_recipes_by_name(self, page: int, page_size: int, name: str, sort_method: str = 'name') -> List[Recipe]:
    #     pass
    #
    # def get_recipes_by_date(self, page: int, page_size: int, target_date: str, sort_method: str = 'name') -> List[
    #     Recipe]:
    #     pass
    #
    # def get_recipes_by_author(self, page: int, page_size: int, author: Author, sort_method: str = 'name') -> List[
    #     Recipe]:
    #     pass
    #
    # def get_recipes_by_category(self, page: int, page_size: int, category: Category, sort_method: str = 'name') -> List[
    #     Recipe]:
    #     pass
    #
    # def get_recipes_by_rating(self, page: int, page_size: int, rating: float, sort_method: str = 'name') -> List[
    #     Recipe]:
    #     pass
    #
    # # endregion
    #
    # # region Review_data Methods to manage Reviews
    # def add_review(self, user: User, review: Review):
    #     pass
    #
    # def get_reviews_for_recipe(self, recipe_id: int) -> List[Review]:
    #     pass
    #
    # def get_reviews_for_user(self, username: str) -> List[Review]:
    #     pass
    #
    # def get_reviews(self, page: int, page_size: int, sort_method: str) -> List[Review]:
    #    pass
    #
    # def get_user_reviews(self, page: int, page_size: int, user: User, sort_method: str) -> List[Review]:
    #     pass
    #
    # def get_recipe_reviews(self, page: int, page_size: int, recipe: Recipe, sort_method: str) -> List[Review]:
    #     pass
    #
    # def get_recipes_reviewed_by_user(self, page: int, page_size: int, user: User, sort_method: str) -> List[Recipe]:
    #     pass
    #
    # def get_review_by_id(self, review_id: int) -> Review:
    #     pass
    #
    # # endregion
    #
    # # region User_favourite_recipes Methods to manage User's favourite Recipes
    # def add_favourite_recipe(self, user: User, recipe: Recipe):
    #     pass
    #
    # def remove_favourite_recipe(self, user: User, recipe: Recipe):
    #     pass
    #
    # def get_favourite_recipes(self, page: int, page_size: int, user: User) -> List[Recipe]:
    #     pass
    #
    # # endregion
    #
    # # region Nutrition_data Methods to manage Nutrition
    # def get_nutritions(self, sorting: bool = False) -> List[Type[Nutrition]]:
    #     pass
    #
    # def get_nutrition(self, nutrition_id: int) -> Nutrition:
    #    pass
    #
    # def add_nutrition(self, nutrition: Nutrition):
    #     pass
    #
    # def add_multiple_nutritions(self, nutritions: List[Nutrition]):
    #    pass
    #
    # def get_number_of_nutritions(self) -> List[Nutrition]:
    #     pass
    #
    # def get_nutritions_for_recipe(self, recipe_id: int) -> List[Nutrition]:
    #     pass
    #
    # def get_number_of_nutritions_for_recipe(self, recipe_id: int) -> int:
    #     pass
    #
    # # endregion
    #
    # def _populate_recipe_data(self, recipe: Recipe):
    #     """
    #     Populate a Recipe object with related data (images, ingredients, instructions)
    #     to maintain consistent domain model interface between memory and database repositories.
    #     """
    #     if recipe is None:
    #         return
    #
    #     # Use the same session context
    #     with self._session_cm as scm:
    #         self._populate_recipe_data_in_session(recipe, scm.session)
    #
    # def _populate_recipe_data_in_session(self, recipe: Recipe, session):
    #     """
    #     Populate a Recipe object with related data using the provided session.
    #     """
    #     if recipe is None:
    #         return
    #
    #     # Load and populate images
    #     recipe_images = session.query(RecipeImage).filter(
    #         RecipeImage._RecipeImage__recipe_id == recipe.id
    #     ).order_by(RecipeImage._RecipeImage__position).all()
    #
    #     if recipe_images:
    #         image_urls = [img.url for img in recipe_images]
    #         recipe._Recipe__images = image_urls
    #     else:
    #         print(f"DEBUG: No images found for recipe {recipe.id}")
    #
    #     # TODO: Load and populate ingredients
    #
    #     # TODO: Load and populate instructions
    #
    #
    # # region RecipeImage Methods
    # def add_recipe_image(self, recipe_image: RecipeImage):
    #     pass
    #
    # def add_multiple_recipe_images(self, recipe_images: List[RecipeImage]):
    #     with self._session_cm as scm:
    #         for recipe_image in recipe_images:
    #             scm.session.add(recipe_image)
    #         scm.commit()
    #
    # def get_recipe_images(self, recipe_id: int) -> List[RecipeImage]:
    #     pass
    #
    # # endregion
    #
    # # region RecipeIngredient Methods
    # def add_recipe_ingredient(self, recipe_ingredient: RecipeIngredient):
    #     pass
    #
    # def add_multiple_recipe_ingredients(self, recipe_ingredients: List[RecipeIngredient]):
    #     pass
    #
    # def get_recipe_ingredients(self, recipe_id: int) -> List[RecipeIngredient]:
    #     pass
    #
    # # endregion
    #
    # # region RecipeInstruction Methods
    # def add_recipe_instruction(self, recipe_instruction: RecipeInstruction):
    #     pass
    #
    # def add_multiple_recipe_instructions(self, recipe_instructions: List[RecipeInstruction]):
    #     pass
    #
    # def get_recipe_instructions(self, recipe_id: int) -> List[RecipeInstruction]:
    #     pass
    #
    # # endregion
