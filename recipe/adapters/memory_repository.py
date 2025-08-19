from typing import List
import ast

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.adapters.repository import AbstractRepository
from recipe.adapters.datareader.csvdatareader import CSVDataReader
from datetime import datetime
import re


class MemoryRepository(AbstractRepository):

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


    def populate(self):

        reader = CSVDataReader()
        rows = reader.read()

        for row in rows:

            #reading and storing data from each column from the csv file
            recipeid = int(row["RecipeId"])
            recipename = row["Name"]
            authorid = int(row["AuthorId"])
            authorname = row["AuthorName"]
            recipecooktime = int(row["CookTime"])
            recipepreptime = int(row["PrepTime"])
            recipetotaltime = int(row["TotalTime"])
            recipedate = datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', row["DatePublished"]), "%d %b %Y")
            recipedescription = row["Description"]
            recipeimages = ast.literal_eval(row["Images"])
            categoryname = row["RecipeCategory"]
            ingredientquantities = ast.literal_eval(row["RecipeIngredientQuantities"])
            ingredientparts = ast.literal_eval(row["RecipeIngredientParts"])
            calories = ast.literal_eval(row["Calories"])

            fatcontent = ast.literal_eval(row["FatContent"])
            saturatedfatcontent = ast.literal_eval(row["SaturatedFatContent"])
            cholesterolcontent = ast.literal_eval(row["CholesterolContent"])
            sodiumcontent = ast.literal_eval(row["SodiumContent"])
            carbohydratecontent = ast.literal_eval(row["CarbohydrateContent"])
            fibercontent = ast.literal_eval(row["FiberContent"])
            sugarcontent = ast.literal_eval(row["SugarContent"])
            proteincontent = ast.literal_eval(row["ProteinContent"])

            recipeservings = ast.literal_eval(row["RecipeServings"])
            recipeyield = ast.literal_eval(row["RecipeYield"])

            recipeinstructions = ast.literal_eval(row["RecipeInstructions"])

            author = Author(author_id = authorid, name = authorname)
            category = Category(name = categoryname)

            


            recipe = Recipe(recipe_id=int(row["RecipeId"]), name=row["Name"], author=author)
            recipe.cook_time = int(row["CookTime"])
            recipe.preparation_time = int(row["PrepTime"])

            date_str = row["DatePublished"]
            clean_date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
            recipe.date = datetime.strptime(clean_date_str, "%d %b %Y")

            recipe.description = row["Description"]
            recipe.images = ast.literal_eval(row["Images"])


            recipe.ingredients = row["RecipeIngredientParts"]
            recipe.ingredient_quantities = row["RecipeIngredientQuantities"]

            recipe.category = category

            recipe.rating = None

            recipe.nutrition = None  # to be implemented after merging branches

            servings = row["RecipeServings"]
            if servings != "NA":
                recipe.servings = int(servings)  # if "NA" then we revert to the default value -> "Not Specified"

            recipe_yield = row["RecipeYield"]
            if recipe_yield != "NA":
                recipe.recipe_yield = recipe_yield  # if "NA" then we revert to the default value -> "Not Specified"

            recipe.instructions = [str(inst) for inst in row["RecipeInstructions"]]

            category.add_recipe(recipe)
            author.add_recipe(recipe)

            self.author_add(author)
            self.recipe_add(recipe)
            self.category_add(category)


