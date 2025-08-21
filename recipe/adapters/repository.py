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
    def author_add(self, author):
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
    def category_add(self, category):
        """Adds a Category to the repository"""
        raise NotImplementedError
    @abc.abstractmethod
    def category_get_by_name(self, category_name) -> Category:
        """Returns a Category by its name"""
        raise NotImplementedError

    @abc.abstractmethod
    def category_get_all(self):
        """Returns a list of Categories"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_add(self, recipe):
        """Adds a Recipe to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_by_name(self, recipe_name) -> Recipe:
        """Returns a Recipe by its name"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_all(self):
        """Returns a list of Recipes"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipes_get_all_by_category(self, category_name) -> List[Recipe]:
        """Returns a list of Recipes by category"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_dict_add(self, recipe):
        """Adds a Recipe to the dictionary"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_by_id(self, recipe_id):
        """Returns a Recipe by its id"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_quantity(self):
        """Returns the quantity the recipes"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_random(self):
        """Returns a random Recipe"""
        raise NotImplementedError

    @abc.abstractmethod
    def recipe_get_latest(self, num: int):
        """Returns the latest Recipe"""
        raise NotImplementedError

    """
    @abc.abstractmethod
    def nutrition_add(self, recipe):
        raise NotImplementedError

    @abc.abstractmethod
    def nutrition_get_all(self):
        raise NotImplementedError
    """
