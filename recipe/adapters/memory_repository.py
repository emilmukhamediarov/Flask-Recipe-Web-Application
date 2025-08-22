import random
from typing import List
import ast
from bisect import insort_left

from recipe.adapters.datareader.csv_data_reader import CSVDataReader
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.adapters.repository import AbstractRepository
from datetime import datetime
import re


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__authors = list()
        self.__categories = list()
        self.__nutrition = list()
        self.__recipes = list()
        self.__recipes_dict = dict()

    def author_add(self, new_author):
        if not isinstance(new_author, Author):
            raise ValueError("Author must be provided as an instance of Author.")
        if new_author not in self.__authors:
            insort_left(self.__authors, new_author)

    def author_get_by_name(self, author_name):
        return next((author for author in self.__authors if author.name == author_name), None)

    def author_get_all(self) -> List[Author]:
        return self.__authors

    def category_add(self, category):
        if not isinstance(category, Category):
            raise ValueError("Category must be provided as an instance of Category.")
        # if category not in self.__categories:
        #     self.__categories.append(category)
        # omg equality check
        if self.category_get_by_name(category.name) is None:
            self.__categories.append(category)

    def category_get_by_name(self, category_name):
        return next((category for category in self.__categories if category.name == category_name), None)

    def category_get_all(self):
        return self.__categories

    def recipe_add(self, recipe):
        if not isinstance(recipe, Recipe):
            raise ValueError("Recipe must be provided as an instance of Recipe.")
        if recipe not in self.__recipes:
            insort_left(self.__recipes, recipe)

    def recipe_get_by_name(self, recipe_name):
        return next((recipe for recipe in self.__recipes if recipe.name == recipe_name), None)

    def recipe_get_all(self):
        return self.__recipes

    def recipes_get_all_by_category(self, category_name):
        return [recipe for recipe in self.__recipes if recipe.category.name == category_name]

    def recipe_dict_add(self, recipe):
        if not isinstance(recipe, Recipe):
            raise ValueError("Recipe must be provided as an instance of Recipe.")
        self.__recipes_dict[recipe.id] = recipe

    def recipe_get_by_id(self, recipe_id):
        if not recipe_id in self.__recipes_dict:
            raise ValueError("Recipe with id {} not found".format(recipe_id))
        return self.__recipes_dict[recipe_id]

    def recipe_get_quantity(self):
        return len(self.__recipes)

    def recipe_get_random(self):
        return random.choice(self.__recipes)

    def recipe_get_latest(self, num: int):
        return self.__recipes[-num:]

    """
    def nutrition_add(self, nutrition):
        if not isinstance(nutrition, Nutrition):
            raise ValueError("Nutrition must be provided as an instance of Nutrition.")
        if nutrition not in self.__nutrition:
            insort_left(self.__nutrition, nutrition)

    def nutrition_get_all(self):
        return self.__nutrition
    """


def populate(data_path, repo):
    reader = CSVDataReader(data_path)
    data = reader.read()

    for row in data:

        #reading and storing data of each column from the csv file
        recipe_id = int(row["RecipeId"])
        recipe_name = row["Name"]
        author_id = int(row["AuthorId"])
        author_name = row["AuthorName"]
        recipe_cook_time = int(row["CookTime"])
        recipe_prep_time = int(row["PrepTime"])
        recipe_total_time = int(row["TotalTime"])
        recipe_date = datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', row["DatePublished"]), "%d %b %Y")
        recipe_description = row["Description"]
        recipe_images = ast.literal_eval(row["Images"])
        category_name = row["RecipeCategory"]
        ingredient_quantities = ast.literal_eval(row["RecipeIngredientQuantities"])
        ingredient_parts = ast.literal_eval(row["RecipeIngredientParts"])

        calories = float(row["Calories"])
        fat_content = float(row["FatContent"])
        saturated_fat_content = float(row["SaturatedFatContent"])
        cholesterol_content = float(row["CholesterolContent"])
        sodium_content = float(row["SodiumContent"])
        carbohydrate_content = float(row["CarbohydrateContent"])
        fiber_content = float(row["FiberContent"])
        sugar_content = float(row["SugarContent"])
        protein_content = float(row["ProteinContent"])

        recipe_servings = row["RecipeServings"]
        recipe_yield = row["RecipeYield"]

        recipe_instructions = ast.literal_eval(row["RecipeInstructions"])

        author = Author(author_id = author_id, name = author_name)
        category = Category(name = category_name)
        existing = repo.category_get_by_name(category_name)
        if existing is None:
            category = Category(name=category_name)
            repo.category_add(category)
        else:
            category = existing

        nutrition_data = {}
        nutrition = Nutrition(nutrition_data)
        nutrition.data["Calories"] = calories
        nutrition.data["Fat"] = fat_content
        nutrition.data["Saturated Fat"] =  saturated_fat_content
        nutrition.data["Cholesterol"] = cholesterol_content
        nutrition.data["Sodium"] = sodium_content
        nutrition.data["Carbohydrates"] = carbohydrate_content
        nutrition.data["Fiber"] = fiber_content
        nutrition.data["Sugar"] = sugar_content
        nutrition.data["Protein"] = protein_content

        recipe = Recipe(recipe_id = recipe_id, name = recipe_name, author = author)

        recipe.nutrition = nutrition
        recipe.category = category

        recipe.cook_time = recipe_cook_time
        recipe.preparation_time = recipe_prep_time
        recipe.total_time = recipe_total_time
        recipe.date = recipe_date
        recipe.description = recipe_description
        recipe.images = recipe_images
        recipe.ingredients = ingredient_parts
        recipe.ingredient_quantities = ingredient_quantities

        if recipe_servings != "NA":
            recipe.servings = int(recipe_servings)  # if "NA" then we revert to the default value -> "Not Specified"

        if recipe_yield != "NA":
            recipe.recipe_yield = recipe_yield  # if "NA" then we revert to the default value -> "Not Specified"

        recipe.instructions = recipe_instructions

        recipe.rating = None

        if recipe not in category.recipes:
            category.add_recipe(recipe)

        # do i need this below?
        # category.add_recipe(recipe)
        author.add_recipe(recipe)

        repo.author_add(author)
        repo.recipe_add(recipe)
        repo.recipe_dict_add(recipe)
        repo.category_add(category)



