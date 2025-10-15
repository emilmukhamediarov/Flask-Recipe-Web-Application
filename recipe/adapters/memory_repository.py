import random
from typing import List

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.domainmodel.favourite import Favourite
from recipe.adapters.repository import AbstractRepository

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__authors = list()
        self.__categories = list()
        self.__recipes = list()
        self.__reviews = list()
        self.__favourites = list()
        self.__users = dict()

    def author_add(self, new_author) -> None:
        if not isinstance(new_author, Author):
            raise ValueError("Author must be provided as an instance of Author.")
        if new_author not in self.__authors:
            self.__authors.append(new_author)

    def author_get_by_name(self, author_name) -> Author:
        return next((author for author in self.__authors if author.name == author_name), None)

    def author_get_by_id(self, author_id) -> Author:
        return next((author for author in self.__authors if author.id == author_id), None)

    def author_get_all(self) -> List[Author]:
        return self.__authors

    def author_get_all_names(self) -> List[Author]:
        return sorted(author.name for author in self.__authors)

    def category_add(self, category) -> None:
        if not isinstance(category, Category):
            raise ValueError("Category must be provided as an instance of Category.")
        if category not in self.__categories:
            self.__categories.append(category)

    def category_add_by_name(self, category_name) -> Category:
        if not isinstance(category_name, str):
            raise ValueError("Category name must be provided as an instance of str.")
        category = next((category for category in self.__categories if category.name == category_name), None)
        if category is None:
            category = Category(category_name)
            self.__categories.append(category)
        return category

    def category_get_by_name(self, category_name) -> Category:
        return next((category for category in self.__categories if category.name == category_name), None)

    def category_get_all(self) -> List[Category]:
        return self.__categories

    def category_get_all_names(self) -> List[str]:
        return [category.name for category in self.__categories]

    def recipe_add(self, recipe) -> None:
        if not isinstance(recipe, Recipe):
            raise ValueError("Recipe must be provided as an instance of Recipe.")
        if recipe not in self.__recipes:
            self.__recipes.append(recipe)

    def recipe_get_all(self) -> List[Recipe]:
        return self.__recipes

    def recipe_get_by_name(self, recipe_name) -> Recipe:
        return next((recipe for recipe in self.__recipes if recipe.name == recipe_name), None)

    def recipes_get_all_by_category(self, category_name) -> List[Recipe]:
        return [recipe for recipe in self.__recipes if recipe.category.name == category_name]

    def recipe_get_by_id(self, recipe_id) -> Recipe:
        return next((recipe for recipe in self.__recipes if recipe.id == recipe_id), None)

    def recipe_get_quantity(self) -> int:
        return len(self.__recipes)

    def recipe_get_random(self) -> Recipe:
        return random.choice(self.__recipes)

    def recipe_get_latest(self, num: int) -> List[Recipe]:
        return self.__recipes[-num:]

    def user_add(self, user : User):
        self.__users[user.username] = user

    def user_get_by_username(self, username: str):
        return self.__users.get(username)

    def user_get_by_id(self, user_id : int) -> User:
        return next((u for u in self.__users.values() if u.id == user_id), None)

    def reviews_add(self, review : Review) -> None:
        if not isinstance(review, Review):
            raise ValueError("Review must be provided as an instance of Recipe.")
        if review not in self.__reviews:
            user = self.user_get_by_id(review.user_id)
            user.add_review(review)
            self.__reviews.append(review)

    def reviews_remove(self, review : Review) -> None:
        if not isinstance(review, Review):
            raise ValueError("Review must be provided as an instance of Recipe.")
        if review in self.__reviews:
            self.__reviews.remove(review)

    def reviews_get_by_id(self, review_id : int) -> Review:
        return next((review for review in self.__reviews if review.id == review_id), None)

    def reviews_get_all_by_user_id(self, user_id : int) -> List[Review]:
        return [review for review in self.__reviews if review.user_id == user_id]

    def reviews_get_all_by_recipe_id(self, recipe_id : int) -> List[Review]:
        return [review for review in self.__reviews if review.recipe_id == recipe_id]

    def favourite_add(self, favourite) -> None:
        if favourite not in self.__favourites:
            self.__favourites.append(favourite)

    def favourite_remove(self, user_id : int, recipe_id : int) -> None:
        f = next((f for f in self.__favourites if f.user_id == user_id and f.recipe_id == recipe_id), None)
        if f:
            self.__favourites.remove(f)

    def favourite_get_all(self) -> List[Recipe]:
        return self.__favourites

    def favourite_get_all_by_user_id(self, user_id: int) -> List[Favourite]:
        return [favourite for favourite in self.__favourites if user_id == favourite.user_id]

    def add_multiple_recipes(self, recipes: List[Recipe]):
        self.__recipes = recipes

    def add_multiple_categories(self, categories: List[Category]):
        self.__categories = categories

    def add_multiple_authors(self, authors: List[Author]):
        self.__authors = authors



