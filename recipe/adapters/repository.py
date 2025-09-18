import abc
from typing import List

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

repo_instance = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def author_add(self, author) -> None:
        """Adds an Author to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def author_get_by_name(self, author_name) -> Author:
        """Returns an Author by their name"""
        raise NotImplementedError

    @abc.abstractmethod
    def author_get_all(self) -> List[Author]:
        """Returns a list of Authors"""
        raise NotImplementedError

    @abc.abstractmethod
    def author_get_all_names(self) -> List[Author]:
        """Returns a list of Author names"""
        raise NotImplementedError

    @abc.abstractmethod
    def category_add(self, category) -> None:
        """Adds a Category to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def category_get_by_name(self, category_name) -> Category:
        """Returns a Category by its name"""
        raise NotImplementedError

    @abc.abstractmethod
    def category_add_by_name(self, category_name) -> Category:
        """Creates a new Category with the given name and returns the new object"""
        raise NotImplementedError

    @abc.abstractmethod
    def category_get_all(self) -> List[Category]:
        """Returns a list of Categories"""
        raise NotImplementedError

    @abc.abstractmethod
    def category_get_all_names(self) -> List[str]:
        """Returns a list of Category Names"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_add(self, recipe) -> None:
        """Adds a Recipe to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_by_name(self, recipe_name) -> Recipe:
        """Returns a Recipe by its name"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_all(self) -> List[Recipe]:
        """Returns a list of Recipes"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipes_get_all_by_category(self, category_name) -> List[Recipe]:
        """Returns a list of Recipes by category"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_by_id(self, recipe_id) -> Recipe:
        """Returns a Recipe by its id"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_quantity(self) -> int:
        """Returns the quantity the recipes"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_random(self) -> Recipe:
        """Returns a random Recipe"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_latest(self, num: int) -> List[Recipe]:
        """Returns the latest Recipe"""
        raise NotImplementedError

    @abc.abstractmethod
    def user_add(self, user: User):
        """Adds User to the dictionary"""
        raise NotImplementedError

    @abc.abstractmethod
    def user_get_by_username(self, username: str) -> User:
        """Returns the User by username"""
        raise NotImplementedError

    @abc.abstractmethod
    def user_get_by_id(self, user_id: int) -> User:
        """Returns the User by id"""
        raise NotImplementedError

    @abc.abstractmethod
    def reviews_add(self, review) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def reviews_get_by_id(self, review_id: int) -> Review:
        raise NotImplementedError

    @abc.abstractmethod
    def reviews_get_all_by_user_id(self, user_id: int) -> List[Review]:
        raise NotImplementedError

    @abc.abstractmethod
    def reviews_get_all_by_recipe_id(self, recipe_id: int) -> List[Review]:
        raise NotImplementedError