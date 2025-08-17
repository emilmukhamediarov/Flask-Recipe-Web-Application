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
    def author_get_all(self) -> List[Author]:
        """Returns a list of Authors"""
        raise NotImplementedError

    @abc.abstractmethod
    def category_add(self, category):
        """Adds a Category to the repository"""
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
    def recipe_get_all(self):
        """Returns a list of Recipes"""
        raise NotImplementedError

    @abc.abstractmethod
    def nutrition_add(self, recipe):
        """Adds a Nutrition to the repository"""
        raise NotImplementedError

    @abc.abstractmethod
    def nutrition_get_all(self):
        """Returns a list of Nutritions"""
        raise NotImplementedError
