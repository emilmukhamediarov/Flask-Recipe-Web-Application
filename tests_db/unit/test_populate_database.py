from sqlalchemy import select, inspect
from recipe.adapters.orm import mapper_registry
from datetime import datetime


def test_database_populate_inspect_table_names(database_engine):
    inspector = inspect(database_engine)
    tables = inspector.get_table_names()


    assert 'authors' in tables
    assert 'categories' in tables
    assert 'favourites' in tables
    assert 'nutrition' in tables
    assert 'recipe_images' in tables
    assert 'recipe_ingredients' in tables
    assert 'recipe_instructions' in tables
    assert 'recipes' in tables
    assert 'reviews' in tables
    assert 'users' in tables


    assert inspector.get_table_names(
    ) == ['authors', 'categories', 'favourites', 'nutrition',
          'recipe_images', 'recipe_ingredients', 'recipe_instructions', 'recipes', 'reviews', 'users']



def test_database_populate_all_authors(database_engine):
    inspector = inspect(database_engine)
    authors_table_name = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        select_statement = select(mapper_registry.metadata.tables[authors_table_name])
        result = connection.execute(select_statement)
        authors = []
        for row in result:
            authors.append((row[0], row[1]))

        assert len(authors) > 0
        id, name = authors[0]
        assert isinstance(id, int)
        assert isinstance(name, str)
        assert name == 'Carole Reu'
        assert id == 1530


def test_database_populate_all_categories(database_engine):
    columns_table = mapper_registry.metadata.tables['categories']

def test_database_populate_all_favourites(database_engine):
    favourites_table = mapper_registry.metadata.tables['favourites']


def test_database_populate_all_recipes(database_engine):
    recipes_table = mapper_registry.metadata.tables['recipes']

    select_stmt = select(
        recipes_table.c.id,
        recipes_table.c.name,
        recipes_table.c.description,
        recipes_table.c.cook_time,
        recipes_table.c.preparation_time,
        recipes_table.c.total_time,
        recipes_table.c.date,
        recipes_table.c.rating,
        recipes_table.c.servings,
        recipes_table.c.recipe_yield,
        recipes_table.c.author_id,
        recipes_table.c.category_id
    )

    with database_engine.connect() as connection:
        result = connection.execute(select_stmt)
        rows = list(result)

    assert 1533 in rows[0]
    assert rows[0] == (38, 'Low-Fat Berry Blue Frozen Dessert', 'Make and share this Low-Fat Berry Blue Frozen Dessert recipe from Food.com.', 1440, 45, 1485, datetime(2009, 8, 9, 0, 0), None, '4', 'Not specified', 1533, 568)
    assert 'Chocolate Cream Meringue Pie' in rows[49]
    assert rows[49] == (232, 'Chocolate Cream Meringue Pie', 'Make and share this Chocolate Cream Meringue Pie recipe from Food.com.', 19, 35, 54, datetime(2012, 8, 21, 0, 0), None, '8', 'Not specified', 1530, 573)

    recipes = [(r[0], r[1]) for r in rows]

    assert len(recipes) == 50

    assert recipes[0] == (38, 'Low-Fat Berry Blue Frozen Dessert')
    assert recipes[1] == (40, 'Best Lemonade')



def test_database_populate_all_nutrition(database_engine):
    inspector = inspect(database_engine)
    # use the exact table object from mapper metadata
    nutrition_table = mapper_registry.metadata.tables['nutrition']

    select_stmt = select(
        nutrition_table.c.id,
        nutrition_table.c.calories,
        nutrition_table.c.fat,
        nutrition_table.c.saturated_fat,
        nutrition_table.c.cholesterol,
        nutrition_table.c.sodium
    )
    with database_engine.connect() as connection:
        result = connection.execute(select_stmt)
        nutrients = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in result]


    assert len(nutrients) == 50
    assert isinstance(nutrients[0][0], int)
    assert isinstance(nutrients[0][1], float)
    assert nutrients[0][0] == 1101
    assert nutrients[0][1] == 170.9
    assert nutrients[0][2] == 2.5
    assert nutrients[0][3] == 1.3
    assert nutrients[0][4] == 8
    assert nutrients[0][5] == 29.8

def test_database_populate_all_recipe_images(database_engine):
    recipe_images_table = mapper_registry.metadata.tables['recipe_images']



def test_database_populate_all_recipe_ingredients(database_engine):
    recipe_ingredients_table = mapper_registry.metadata.tables['recipe_ingredients']


def test_database_populate_all_recipe_instructions(database_engine):
    recipe_instructions_table = mapper_registry.metadata.tables['recipe_instructions']




def test_database_populate_all_review(database_engine):
    reviews_table = mapper_registry.metadata.tables['reviews']



def test_database_populate_all_users(database_engine):
    users_table = mapper_registry.metadata.tables['users']