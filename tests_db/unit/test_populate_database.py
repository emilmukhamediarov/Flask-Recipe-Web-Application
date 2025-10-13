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
    categories_table = mapper_registry.metadata.tables['categories']

    select_statement = select(categories_table.c.id, categories_table.c.name).order_by(categories_table.c.id)

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        rows = list(result)

    assert len(rows) == 27

    assert isinstance(rows[0][0], int)
    assert isinstance(rows[0][1], str)

    assert rows[0][0] == 514
    assert rows[0][1] == 'Frozen Desserts'
    assert rows[1][0] == 515
    assert rows[1][1] == 'Beverages'



def test_database_populate_all_favourites(database_engine):
    favourites_table = mapper_registry.metadata.tables['favourites']

    select_statement = select(favourites_table.c.id, favourites_table.c.user_id, favourites_table.c.recipe_id)

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        rows = list(result)


    if rows:
        assert isinstance(rows[0][0], int)
        assert isinstance(rows[0][1], int)
        assert isinstance(rows[0][2], int)



def test_database_populate_all_recipes(database_engine):
    recipes_table = mapper_registry.metadata.tables['recipes']

    select_statement = select(
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
        result = connection.execute(select_statement)
        rows = list(result)

    assert 'Low-Fat Berry Blue Frozen Dessert' and 'Make and share this Low-Fat Berry Blue Frozen Dessert recipe from Food.com.' and 1440 and 45 and 1485 in rows[0]
    assert 'Chocolate Cream Meringue Pie' and 'Make and share this Chocolate Cream Meringue Pie recipe from Food.com.' and 19 and 35 and 54 in rows[49]

    recipes = [(r[0], r[1]) for r in rows]

    assert len(recipes) == 50

    assert recipes[0] == (38, 'Low-Fat Berry Blue Frozen Dessert')
    assert recipes[1] == (40, 'Best Lemonade')



def test_database_populate_all_nutrition(database_engine):
    nutrition_table = mapper_registry.metadata.tables['nutrition']

    select_statement = select(
        nutrition_table.c.id,
        nutrition_table.c.calories,
        nutrition_table.c.fat,
        nutrition_table.c.saturated_fat,
        nutrition_table.c.cholesterol,
        nutrition_table.c.sodium
    )
    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        nutrients = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in result]


    assert len(nutrients) == 50
    assert isinstance(nutrients[0][0], int)
    assert isinstance(nutrients[0][1], float)
    assert nutrients[0][1] == 170.9
    assert nutrients[0][2] == 2.5
    assert nutrients[0][3] == 1.3
    assert nutrients[0][4] == 8
    assert nutrients[0][5] == 29.8



def test_database_populate_all_recipe_images(database_engine):
    recipe_images_table = mapper_registry.metadata.tables['recipe_images']

    select_statement = select(
        recipe_images_table.c.id,
        recipe_images_table.c.url,
        recipe_images_table.c.recipe_id
    )

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        rows = list(result)


    assert len(rows) == 175
    assert isinstance(rows[0][0], int)
    assert isinstance(rows[0][1], str)
    assert isinstance(rows[0][2], int)
    assert 'https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/YUeirxMLQaeE1h3v3qnM_229%20berry%20blue%20frzn%20dess.jpg' and 38 in rows[0]

    assert 38 in rows[0]




def test_database_populate_all_recipe_ingredients(database_engine):
    recipe_ingredients_table = mapper_registry.metadata.tables['recipe_ingredients']

    select_statement = select(
        recipe_ingredients_table.c.id,
        recipe_ingredients_table.c.quantity,
        recipe_ingredients_table.c.ingredient,
        recipe_ingredients_table.c.recipe_id
    )

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        rows = list(result)

    assert len(rows) > 0
    first = rows[0]
    assert isinstance(first[0], int)
    assert isinstance(first[1], str)
    assert isinstance(first[2], str)
    assert isinstance(first[3], int)

    assert first[1] == '4'
    assert first[2] == 'blueberries'
    assert first[3] == 38


    assert rows[5][1] == '1'
    assert rows[5][2] == 'lemons, rind of'
    assert rows[5][3] == 40



def test_database_populate_all_recipe_instructions(database_engine):
    recipe_instructions_table = mapper_registry.metadata.tables['recipe_instructions']

    select_statement = select(
        recipe_instructions_table.c.id,
        recipe_instructions_table.c.step,
        recipe_instructions_table.c.recipe_id
    )

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        rows = list(result)

    assert len(rows) > 0
    first = rows[0]
    assert isinstance(first[0], int)
    assert isinstance(first[1], str)
    assert isinstance(first[2], int)

    assert first[0] == 1
    assert first[1] == 'Cover marshmallows and cranberries with sugar; chill overnight.'
    assert rows[1][1] == 'Add apples, grapes, walnuts, salt and whipping cream.'
    assert rows[1][0] == 2




def test_database_populate_all_review(database_engine):
    reviews_table = mapper_registry.metadata.tables['reviews']

    select_statement = select(
        reviews_table.c.id,
        reviews_table.c.user_id,
        reviews_table.c.recipe_id,
        reviews_table.c.rating,
        reviews_table.c.text,
        reviews_table.c.created_date
    )

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        rows = list(result)

    assert len(rows) == 0

    if rows:
        first = rows[0]
        assert isinstance(first[0], int)
        assert isinstance(first[1], int)
        assert isinstance(first[2], int)
        assert isinstance(first[3], int)
        assert isinstance(first[4], str)


def test_database_populate_all_users(database_engine):
    users_table = mapper_registry.metadata.tables['users']
    select_statement = select(
        users_table.c.id,
        users_table.c.username,
        users_table.c.password_hash
    )

    with database_engine.connect() as connection:
        result = connection.execute(select_statement)
        rows = list(result)

    assert len(rows) == 0