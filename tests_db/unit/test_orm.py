# tests/unit/test_orm_extended.py
from datetime import datetime
from sqlalchemy import text
import datetime

from recipe.domainmodel.author import Author
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.recipe_ingredient import RecipeIngredient



def test_insert_author(empty_session):
    empty_session.execute(text(
        "INSERT INTO authors (id, name) VALUES (1, 'Gordon Ramsay')"
    ))
    result = empty_session.execute(text("SELECT * FROM authors")).fetchall()
    assert len(result) == 1
    assert result[0][1] == "Gordon Ramsay"


def test_insert_category(empty_session):
    empty_session.execute(text(
        "INSERT INTO categories (id, name) VALUES (1, 'Dessert')"
    ))
    result = empty_session.execute(text("SELECT name FROM categories")).fetchone()
    assert result[0] == "Dessert"


def test_insert_recipe_with_author_category(empty_session):
    empty_session.execute(text("INSERT INTO authors (id, name) VALUES (1, 'Jamie Oliver')"))
    empty_session.execute(text("INSERT INTO categories (id, name) VALUES (1, 'Main Course')"))
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time, author_id, category_id)
        VALUES (1, 'Pasta', 'Tasty Italian dish', 20, 10, 30, 1, 1)
    """))
    result = empty_session.execute(text("SELECT name FROM recipes")).fetchone()
    assert result[0] == "Pasta"


def test_insert_user(empty_session):
    empty_session.execute(text(
        "INSERT INTO users (id, username, password_hash) VALUES (1, 'test_user', 'hashed_pw')"
    ))
    count = empty_session.execute(text("SELECT COUNT(*) FROM users")).scalar()
    assert count == 1



def test_insert_recipe_and_nutrition(empty_session):
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (1, 'Salad', 'Fresh greens', 0, 10, 10)
    """))
    empty_session.execute(text("""
        INSERT INTO nutrition (id, recipe_id, calories, fat, sugar, protein)
        VALUES (1, 1, 120, 5, 3, 4)
    """))
    result = empty_session.execute(text("SELECT recipe_id FROM nutrition")).fetchone()
    assert result[0] == 1


def test_recipe_without_nutrition_allowed(empty_session):
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (2, 'Soup', 'Vegetable soup', 30, 10, 40)
    """))
    result = empty_session.execute(text("SELECT * FROM recipes WHERE id = 2")).fetchone()
    assert result is not None



def test_insert_recipe_images(empty_session):
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (4, 'Burger', 'Juicy burger', 15, 10, 25)
    """))
    empty_session.execute(text("""
        INSERT INTO recipe_images (url, recipe_id) VALUES ('image_url.jpg', 4)
    """))
    result = empty_session.execute(text("SELECT COUNT(*) FROM recipe_images")).scalar()
    assert result == 1


def test_insert_recipe_instructions(empty_session):
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (5, 'Pancakes', 'Fluffy pancakes', 10, 10, 20)
    """))
    empty_session.execute(text("""
        INSERT INTO recipe_instructions (step, recipe_id) VALUES ('Mix ingredients', 5)
    """))
    result = empty_session.execute(text("SELECT step FROM recipe_instructions")).fetchone()
    assert "Mix ingredients" in result[0]


def test_insert_recipe_ingredients(empty_session):
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (6, 'Smoothie', 'Fruit blend', 0, 5, 5)
    """))
    empty_session.execute(text("""
        INSERT INTO recipe_ingredients (quantity, ingredient, recipe_id)
        VALUES ('1 cup', 'Strawberries', 6)
    """))
    result = empty_session.execute(text("SELECT ingredient FROM recipe_ingredients")).fetchone()
    assert result[0] == "Strawberries"


def test_insert_review(empty_session):
    empty_session.execute(text("INSERT INTO users (id, username, password_hash) VALUES (1, 'user1', 'pw')"))
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (7, 'Soup', 'Hot soup', 20, 10, 30)
    """))
    now = datetime.datetime.now()
    empty_session.execute(text(f"""
        INSERT INTO reviews (user_id, recipe_id, rating, text, created_date)
        VALUES (1, 7, 5, 'Excellent!', '{now}')
    """))
    result = empty_session.execute(text("SELECT rating FROM reviews")).fetchone()
    assert result[0] == 5


def test_insert_favourite(empty_session):
    empty_session.execute(text("INSERT INTO users (id, username, password_hash) VALUES (2, 'user2', 'pw')"))
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (8, 'Curry', 'Spicy curry', 30, 15, 45)
    """))
    empty_session.execute(text("""
        INSERT INTO favourites (user_id, recipe_id) VALUES (2, 8)
    """))
    result = empty_session.execute(text("SELECT * FROM favourites")).fetchone()
    assert result[1] == 2 and result[2] == 8


def test_duplicate_favourite_not_allowed(empty_session):
    empty_session.execute(text("INSERT INTO users (id, username, password_hash) VALUES (3, 'user3', 'pw')"))
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (9, 'Pizza', 'Cheesy pizza', 20, 20, 40)
    """))
    empty_session.execute(text("INSERT INTO favourites (user_id, recipe_id) VALUES (3, 9)"))
    try:
        empty_session.execute(text("INSERT INTO favourites (user_id, recipe_id) VALUES (3, 9)"))
        empty_session.commit()
        assert False, "Expected UNIQUE constraint failure"
    except Exception as e:
        assert "UNIQUE" in str(e)


def test_count_recipes(empty_session):
    for i in range(10):
        empty_session.execute(text(f"""
            INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
            VALUES ({i+10}, 'Recipe{i}', 'Description{i}', 5, 5, 10)
        """))
    count = empty_session.execute(text("SELECT COUNT(*) FROM recipes")).scalar()
    assert count >= 10


def test_average_rating(empty_session):
    empty_session.execute(text("INSERT INTO users (id, username, password_hash) VALUES (4, 'user4', 'pw')"))
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time)
        VALUES (20, 'Pasta Carbonara', 'Creamy pasta', 20, 15, 35)
    """))
    now = datetime.datetime.now()
    for rating in [5, 4, 3]:
        empty_session.execute(text(f"""
            INSERT INTO reviews (user_id, recipe_id, rating, text, created_date)
            VALUES (4, 20, {rating}, 'Review text', '{now}')
        """))
    avg_rating = empty_session.execute(text("""
        SELECT AVG(rating) FROM reviews WHERE recipe_id = 20
    """)).scalar()
    assert round(avg_rating, 1) == 4.0


def test_join_recipe_and_author(empty_session):
    empty_session.execute(text("INSERT INTO authors (id, name) VALUES (5, 'Heston')"))
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time, author_id)
        VALUES (30, 'Fish', 'Poached fish', 15, 10, 25, 5)
    """))
    result = empty_session.execute(text("""
        SELECT recipes.name, authors.name
        FROM recipes JOIN authors ON recipes.author_id = authors.id
    """)).fetchone()
    assert result == ('Fish', 'Heston')


def test_join_recipe_and_category(empty_session):
    empty_session.execute(text("INSERT INTO categories (id, name) VALUES (2, 'Vegan')"))
    empty_session.execute(text("""
        INSERT INTO recipes (id, name, description, cook_time, preparation_time, total_time, category_id)
        VALUES (31, 'Tofu Bowl', 'Vegan dish', 10, 10, 20, 2)
    """))
    result = empty_session.execute(text("""
        SELECT recipes.name, categories.name
        FROM recipes JOIN categories ON recipes.category_id = categories.id
    """)).fetchone()
    assert result == ('Tofu Bowl', 'Vegan')