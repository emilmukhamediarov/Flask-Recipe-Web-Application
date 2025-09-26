import random
from typing import List
import re
import ast

from recipe.adapters.datareader.csv_data_reader import CSVDataReader
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.domainmodel.favourite import Favourite
from recipe.adapters.repository import AbstractRepository
from datetime import datetime

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

    def author_add_by_id_and_name(self, id : int, name : str) -> Author:
        if not isinstance(name, str) or not isinstance(id, int):
            raise ValueError("Id/Name must be provided as an instance of int/str.")
        author = next((author for author in self.__authors if author.id == id), None)
        if author is None:
            author = Author(id, name)
            self.__authors.append(author)
        return author

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

def populate(data_path, repo):
    reader = CSVDataReader(data_path)
    data = reader.read()

    for row in data:

        #reading and storing data of each column from the csv file
        author_id = int(row["AuthorId"])
        author_name = row["AuthorName"]

        category_name = row["RecipeCategory"]

        recipe_id = int(row["RecipeId"])
        recipe_name = row["Name"]
        recipe_cook_time = int(row["CookTime"])
        recipe_prep_time = int(row["PrepTime"])
        recipe_total_time = int(row["TotalTime"])
        recipe_date = datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', row["DatePublished"]), "%d %b %Y")
        recipe_description = row["Description"]
        recipe_servings = row["RecipeServings"]
        recipe_yield = row["RecipeYield"]

        # Nutrition Information
        calories = float(row["Calories"])
        fat_content = float(row["FatContent"])
        saturated_fat_content = float(row["SaturatedFatContent"])
        cholesterol_content = float(row["CholesterolContent"])
        sodium_content = float(row["SodiumContent"])
        carbohydrate_content = float(row["CarbohydrateContent"])
        fiber_content = float(row["FiberContent"])
        sugar_content = float(row["SugarContent"])
        protein_content = float(row["ProteinContent"])

        recipe_images = ast.literal_eval(row["Images"])
        ingredient_quantities = ast.literal_eval(row["RecipeIngredientQuantities"])
        ingredient_parts = ast.literal_eval(row["RecipeIngredientParts"])
        recipe_instructions = ast.literal_eval(row["RecipeInstructions"])

        nutrition_data = {
            "Calories": calories,
            "Fat": fat_content,
            "Saturated Fat": saturated_fat_content,
            "Cholesterol": cholesterol_content,
            "Sodium": sodium_content,
            "Carbohydrate": carbohydrate_content,
            "Fiber": fiber_content,
            "Sugar": sugar_content,
            "Protein": protein_content,
        }

        author = repo.author_add_by_id_and_name(author_id, author_name)
        category = repo.category_add_by_name(category_name)

        nutrition = Nutrition(nutrition_data)

        recipe = Recipe(recipe_id = recipe_id, name = recipe_name, author = author, category = category)

        recipe.nutrition = nutrition

        recipe.cook_time = recipe_cook_time
        recipe.preparation_time = recipe_prep_time
        recipe.total_time = recipe_total_time
        recipe.date = recipe_date
        recipe.description = recipe_description
        recipe.images = recipe_images
        recipe.ingredients = ingredient_parts
        recipe.ingredient_quantities = ingredient_quantities
        recipe.instructions = recipe_instructions

        recipe.rating = None

        if recipe_servings != "NA":
            recipe.servings = int(recipe_servings)  # if "NA" then we revert to the default value -> "Not Specified"

        if recipe_yield != "NA":
            recipe.recipe_yield = recipe_yield  # if "NA" then we revert to the default value -> "Not Specified"

        category.add_recipe(recipe)
        author.add_recipe(recipe)

        repo.recipe_add(recipe)

    #Enforce minimum 1 recipe to simplify other functions
    if repo.recipe_get_quantity() < 1:
        repo.recipe_add(Recipe(
            0,
            "NO RECIPES FOUND",
            Author(0, ""),
            Category("")
        ))

    #Test user for testing
    test_user = User("TestUser", "test")
    repo.user_add(test_user)



