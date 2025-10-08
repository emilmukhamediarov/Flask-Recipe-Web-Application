from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import registry, relationship
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe_image import RecipeImage

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
    Column('health_score', Float, nullable=True)
)

# Recipes table
recipes_table = Table(
    'recipes', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('description', Text, nullable=False),
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
        '_Nutrition__carbohydrates': nutrition_table.c.carbohydrates,
        '_Nutrition__fiber': nutrition_table.c.fiber,
        '_Nutrition__sugar': nutrition_table.c.sugar,
        '_Nutrition__protein': nutrition_table.c.protein,
        '_Nutrition__health_score': nutrition_table.c.health_score,
        '_Nutrition__recipe': relationship(Recipe, back_populates='_Recipe__nutrition',
        )
    })

    # Recipe mapping
    mapper_registry.map_imperatively(Recipe, recipes_table, properties={
        '_Recipe__id': recipes_table.c.id,
        '_Recipe__name': recipes_table.c.name,
        '_Recipe__description': recipes_table.c.description,
        '_Recipe__nutrition': relationship(
            Nutrition,
            back_populates='_Nutrition__recipe',
            uselist=False,
        ),
    })






