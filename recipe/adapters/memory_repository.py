from typing import List

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.adapters.repository import Abstractrepository


class Memoryrepository(Abstractrepository):

    def __init__(self):
        self.__authors = list()
        self.__categories = list()
        self.__nutrition = list()
        self.__recipes = list()

    def author_add(self, author):
        if not isinstance(author, Author):
            raise ValueError("Author must be provided as an instance of Author.")
        if author not in self.__authors:
            self.__authors.append(author)

    def author_get_all(self) -> List[Author]:
        return self.__authors

    def category_add(self, category):
        if not isinstance(category, Category):
            raise ValueError("Category must be provided as an instance of Category.")
        if category not in self.__categories:
            self.__categories.append(category)

    def category_get_all(self):
        return self.__categories

    def recipe_add(self, recipe):
        if not isinstance(recipe, Recipe):
            raise ValueError("Recipe must be provided as an instance of Recipe.")
        if recipe not in self.__recipes:
            self.__recipes.append(recipe)

    def recipe_get_all(self):
        return self.__recipes

    def nutrition_add(self, nutrition):
        if not isinstance(nutrition, Nutrition):
            raise ValueError("Nutrition must be provided as an instance of Nutrition.")
        if nutrition not in self.__nutrition:
            self.__nutrition.append(nutrition)

    def nutrition_get_all(self):
        return self.__nutrition