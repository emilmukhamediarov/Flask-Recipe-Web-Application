import csv
from pathlib import Path
from typing import List
import re
import ast

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from datetime import datetime

class CSVDataReader:
    def __init__(self, data_path):
        base_dir = Path(__file__).parent.parent.parent
        self._data_path = str(data_path / 'recipes.csv')

        self.__authors = list()
        self.__categories = list()
        self.__recipes = list()


    @property
    def authors(self) -> List[Author]:
        return self.__authors

    @property
    def categories(self) -> List[Category]:
        return self.__categories

    @property
    def recipes(self) -> List[Recipe]:
        return self.__recipes


    def author_add_by_id_and_name(self, id : int, name : str) -> Author:
        if not isinstance(name, str) or not isinstance(id, int):
            raise ValueError("Id/Name must be provided as an instance of int/str.")
        author = next((author for author in self.__authors if author.id == id), None)
        if author is None:
            author = Author(id, name)
            self.__authors.append(author)
        return author

    def category_add_by_name(self, category_name) -> Category:
        if not isinstance(category_name, str):
            raise ValueError("Category name must be provided as an instance of str.")
        category = next((category for category in self.__categories if category.name == category_name), None)
        if category is None:
            category = Category(category_name)
            self.__categories.append(category)
        return category

    def recipe_add(self, recipe) -> None:
        if not isinstance(recipe, Recipe):
            raise ValueError("Recipe must be provided as an instance of Recipe.")
        if recipe not in self.__recipes:
            self.__recipes.append(recipe)

    def read(self):
        if not self._data_path:
            raise FileNotFoundError(f'{self._data_path} does not exist')

        with open(self._data_path, mode='r', encoding='utf-8') as csv_file:
            data = csv.DictReader(csv_file)

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


                author = self.author_add_by_id_and_name(author_id, author_name)
                category = self.category_add_by_name(category_name)

                recipe = Recipe(recipe_id = recipe_id, name = recipe_name, author = author, category = category)


                recipe.cook_time = recipe_cook_time
                recipe.preparation_time = recipe_prep_time
                recipe.total_time = recipe_total_time
                recipe.date = recipe_date
                recipe.description = recipe_description


                images = [RecipeImage(recipe.id, url) for url in recipe_images]
                recipe.images = images

                nutrition = Nutrition (recipe.id, calories, fat_content, saturated_fat_content,
                             cholesterol_content, sodium_content,
                             carbohydrate_content, fiber_content, sugar_content, protein_content)

                recipe.nutrition = nutrition

                ingredients = []

                for i in range(0, min(len(ingredient_quantities), len(ingredient_parts))):
                    new_ingredient = RecipeIngredient(recipe.id, ingredient_quantities[i], ingredient_parts[i])
                    ingredients.append(new_ingredient)


                recipe.ingredients = ingredients


                recipe.ingredients = ingredients
                recipe.ingredient_quantities = ingredient_quantities

                instructions = [RecipeInstruction(recipe.id, step) for step in recipe_instructions]
                recipe.instructions = instructions

                recipe.rating = None

                if recipe_servings != "NA":
                    recipe.servings = int(recipe_servings)  # if "NA" then we revert to the default value -> "Not Specified"

                if recipe_yield != "NA":
                    recipe.recipe_yield = recipe_yield  # if "NA" then we revert to the default value -> "Not Specified"

                self.recipe_add(recipe)