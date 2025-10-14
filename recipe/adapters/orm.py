from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import registry, relationship
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()


# Nutrition table
nutrition_table = Table(
    'nutrition', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, ForeignKey('recipes.id'), unique=True),
    Column('calories', Float, nullable=True),
    Column('fat', Float, nullable=True),
    Column('saturated_fat', Float, nullable=True),
    Column('cholesterol', Float, nullable=True),
    Column('sodium', Float, nullable=True),
    Column('carbohydrates', Float, nullable=True),
    Column('fiber', Float, nullable=True),
    Column('sugar', Float, nullable=True),
    Column('protein', Float, nullable=True),
    Column('health_score', String(255), nullable=True)
)

# Recipes table
recipes_table = Table(
    'recipes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('description', Text, nullable=False),
    Column('cook_time', Integer, nullable=False),
    Column('preparation_time', Integer, nullable=False),
    Column('total_time', Integer, nullable=False),
    Column('date', DateTime, nullable=True),
    Column('rating', Float, nullable=True),
    Column('servings', String(255), nullable=True),
    Column('recipe_yield', String(255), nullable=True),
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('category_id', Integer, ForeignKey('categories.id')),
)

# Authors table
authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
)

# Categories table
categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), nullable=False, unique=True),
)

#RecipeImages table
recipe_images_table = Table(
    'recipe_images', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('url', String(255), nullable=False),
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
)

#RecipeInstructions table
recipe_instructions_table = Table(
    'recipe_instructions', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('step', String(255), nullable=False),
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
)

#RecipeIngredients table
recipe_ingredients_table = Table(
    'recipe_ingredients', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('quantity', String(255), nullable=False),
    Column('ingredient', String(255), nullable=False),
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
)

# Users table
users_table = Table(
    'users', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), nullable=False, unique=True),
    Column('password_hash', String(255), nullable=False),
)

# Reviews table
reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('rating', Integer, nullable=False),
    Column('text', Text, nullable=False),
    Column('created_date', DateTime, nullable=False),
)

# Favourites table
favourites_table = Table(
    'favourites', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    UniqueConstraint('user_id', 'recipe_id', name='uq_user_recipe_favourite')
)


# ORM Mappings
def map_model_to_tables():

    # Nutrition mapping
    mapper_registry.map_imperatively(Nutrition, nutrition_table, properties={
        '_Nutrition__id': nutrition_table.c.id,
        '_Nutrition__calories': nutrition_table.c.calories,
        '_Nutrition__fat': nutrition_table.c.fat,
        '_Nutrition__saturated_fat': nutrition_table.c.saturated_fat,
        '_Nutrition__cholesterol': nutrition_table.c.cholesterol,
        '_Nutrition__sodium': nutrition_table.c.sodium,
        '_Nutrition__carbohydrate': nutrition_table.c.carbohydrates,
        '_Nutrition__fiber': nutrition_table.c.fiber,
        '_Nutrition__sugar': nutrition_table.c.sugar,
        '_Nutrition__protein': nutrition_table.c.protein,
        '_Nutrition__score': nutrition_table.c.health_score,
        '_Nutrition__recipe': relationship(Recipe, back_populates='_Recipe__nutrition',
        )
    })

    # Recipe mapping
    mapper_registry.map_imperatively(Recipe, recipes_table, properties={
        '_Recipe__id': recipes_table.c.id,
        '_Recipe__name': recipes_table.c.name,
        '_Recipe__description': recipes_table.c.description,
        '_Recipe__cook_time': recipes_table.c.cook_time,
        '_Recipe__preparation_time': recipes_table.c.preparation_time,
        '_Recipe__total_time': recipes_table.c.total_time,
        '_Recipe__date': recipes_table.c.date,
        '_Recipe__rating': recipes_table.c.rating,
        '_Recipe__servings': recipes_table.c.servings,
        '_Recipe__recipe_yield': recipes_table.c.recipe_yield,
        '_Recipe__author': relationship(Author, back_populates='_Author__recipes',),
        '_Recipe__category': relationship(Category, back_populates='_Category__recipes',),
        '_Recipe__nutrition': relationship(Nutrition, back_populates='_Nutrition__recipe', uselist=False),
        '_Recipe__images': relationship(RecipeImage, back_populates='_RecipeImage__recipe'),
        '_Recipe__instructions': relationship(RecipeInstruction, back_populates='_RecipeInstruction__recipe'),
        '_Recipe__ingredients': relationship(RecipeIngredient, back_populates='_RecipeIngredient__recipe'),
        '_Recipe__reviews': relationship(Review, back_populates='_Review__recipe'),
        '_Recipe__favourites': relationship(Favourite, back_populates='_Favourite__recipe'),
    })

    # Author mapping
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_Author__id': authors_table.c.id,
        '_Author__name': authors_table.c.name,
        '_Author__recipes': relationship(Recipe, back_populates='_Recipe__author')
    })

    # Category mapping
    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_Category__id': categories_table.c.id,
        '_Category__name': categories_table.c.name,
        '_Category__recipes': relationship(Recipe, back_populates='_Recipe__category')
    })

    # RecipeImages mapping
    mapper_registry.map_imperatively(RecipeImage, recipe_images_table, properties={
        '_RecipeImage__id': recipe_images_table.c.id,
        '_RecipeImage__url': recipe_images_table.c.url,
        '_RecipeImage__recipe_id': recipe_images_table.c.recipe_id,
        '_RecipeImage__recipe': relationship(Recipe, back_populates='_Recipe__images'),
    })

    # RecipeInstructions mapping
    mapper_registry.map_imperatively(RecipeInstruction, recipe_instructions_table, properties={
        '_RecipeInstruction__id': recipe_instructions_table.c.id,
        '_RecipeInstruction__step': recipe_instructions_table.c.step,
        '_RecipeInstruction__recipe_id': recipe_instructions_table.c.recipe_id,
        '_RecipeInstruction__recipe': relationship(Recipe, back_populates='_Recipe__instructions'),
    })

    # RecipeIngredients mapping
    mapper_registry.map_imperatively(RecipeIngredient, recipe_ingredients_table, properties={
        '_RecipeIngredient__id': recipe_ingredients_table.c.id,
        '_RecipeIngredient__quantity': recipe_ingredients_table.c.quantity,
        '_RecipeIngredient__ingredient': recipe_ingredients_table.c.ingredient,
        '_RecipeIngredient__recipe_id': recipe_ingredients_table.c.recipe_id,
        '_RecipeIngredient__recipe': relationship(Recipe, back_populates='_Recipe__ingredients'),
    })

    # User mapping
    mapper_registry.map_imperatively(User, users_table, properties={
        '_User__id': users_table.c.id,
        '_User__username': users_table.c.username,
        '_User__password_hash': users_table.c.password_hash,
        '_User__favourite_recipes': relationship('Favourite', back_populates='_Favourite__user'),
        '_User__reviews': relationship('Review', back_populates='_Review__user'),
    })

    # Review mapping
    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_Review__id': reviews_table.c.id,
        '_Review__user_id': reviews_table.c.user_id,
        '_Review__recipe_id': reviews_table.c.recipe_id,
        '_Review__rating': reviews_table.c.rating,
        '_Review__text': reviews_table.c.text,
        '_Review__date': reviews_table.c.created_date,
        '_Review__user': relationship(User, back_populates='_User__reviews'),
        '_Review__recipe': relationship(Recipe, back_populates='_Recipe__reviews'),
    })

    # Favourite mapping
    mapper_registry.map_imperatively(Favourite, favourites_table, properties={
        '_Favourite__id': favourites_table.c.id,
        '_Favourite__user_id': favourites_table.c.user_id,
        '_Favourite__recipe_id': favourites_table.c.recipe_id,
        '_Favourite__user': relationship(User, back_populates='_User__favourite_recipes'),
        '_Favourite__recipe': relationship(Recipe, back_populates='_Recipe__favourites'),
    })








