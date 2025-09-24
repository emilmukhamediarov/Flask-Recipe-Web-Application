import pytest
from datetime import date, datetime
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User
from recipe.domainmodel.favourite import Favourite

# --- Authors repository methods ---
def test_repository_can_add_an_author(in_memory_repo):
    author = Author (1, 'John')
    in_memory_repo.author_add(author)
    assert in_memory_repo.author_get_by_name('John') is author

def test_repository_can_add_an_author_by_id_and_name(in_memory_repo):
    in_memory_repo.author_add_by_id_and_name(9999, 'Scientist')
    assert in_memory_repo.author_get_by_name('Scientist').name == 'Scientist'

def test_repository_can_get_an_author_by_name(in_memory_repo):
    author = Author (1, 'John')
    in_memory_repo.author_add(author)
    assert in_memory_repo.author_get_by_name("John") is author

def test_repository_can_get_an_author_by_id(in_memory_repo):
    author = Author (9999, 'John')
    in_memory_repo.author_add(author)
    assert in_memory_repo.author_get_by_id(9999) is author

def test_repository_can_get_a_list_of_author_names(in_memory_repo):
    author_names = in_memory_repo.author_get_all_names()
    assert len(author_names) > 1 and type(author_names) is list and type(author_names[0]) is str

def test_repository_can_get_a_list_of_authors(in_memory_repo):
    authors = in_memory_repo.author_get_all()
    assert len(authors) > 1 and type(authors) is list and type(authors[0]) is Author

# --- Recipes repository methods ---
def test_repository_can_add_a_recipe(in_memory_repo):
    author = Author (1, 'John')
    category = Category( 'Milk')
    recipe = Recipe(1, 'Cake', author, category=category)
    in_memory_repo.recipe_add(recipe)
    assert in_memory_repo.recipe_get_by_name('Cake') is recipe

def test_repository_can_get_a_recipe_by_name(in_memory_repo):
    test_recipe = in_memory_repo.recipe_get_all()[10]
    retrieved_recipe = in_memory_repo.recipe_get_by_name(test_recipe.name)
    assert retrieved_recipe.name == test_recipe.name

def test_repository_can_get_all_recipies(in_memory_repo):
    recipies = in_memory_repo.recipe_get_all()
    assert len(recipies) > 1 and type(recipies) is list

def test_repository_can_get_recipes_by_category(in_memory_repo):
    category = Category('Fast good is not good for you')
    author = Author(1, 'John')
    one_recipe = Recipe(1, 'Fast food is delicious', author=author, category=category)
    two_recipe = Recipe(2, 'Another delicious fast food', author=author, category=category)
    in_memory_repo.recipe_add(one_recipe)
    in_memory_repo.recipe_add(two_recipe)
    recipes_by_category = in_memory_repo.recipes_get_all_by_category('Fast good is not good for you')
    assert len(recipes_by_category) == 2 and recipes_by_category[0] is one_recipe

def test_repository_can_get_recipes_by_id(in_memory_repo):
    author = Author (1, 'John')
    category = Category( 'Milk')
    recipe = Recipe(1, 'Cake', author, category=category)
    in_memory_repo.recipe_add(recipe)
    get_recipe_by_id = in_memory_repo.recipe_get_by_id(1)
    assert get_recipe_by_id is recipe

def test_repository_returns_number_of_recipies(in_memory_repo):
    length = in_memory_repo.recipe_get_quantity()
    assert type(length) is int

def test_repository_can_get_a_random_recipe(in_memory_repo):
    random_recipe_one = in_memory_repo.recipe_get_random()
    random_recipe_two = in_memory_repo.recipe_get_random()
    assert type(random_recipe_one) is Recipe and (not(random_recipe_one == random_recipe_two))

def test_repository_can_get_latest_recipe(in_memory_repo):
    latest_recipes = in_memory_repo.recipe_get_latest(5)
    assert len(latest_recipes) == 5

# --- Categories repository methods ---
def test_repository_can_add_a_category(in_memory_repo):
    category = Category('Milk')
    in_memory_repo.category_add(category)
    assert in_memory_repo.category_get_by_name('Milk') is category

def test_repository_can_get_a_category_by_name(in_memory_repo):
    category = Category('Test_category')
    in_memory_repo.category_add(category)
    assert in_memory_repo.category_get_by_name('Test_category') is category

def test_repository_can_add_a_category_by_name(in_memory_repo):
    in_memory_repo.category_add_by_name('Test_category')
    assert in_memory_repo.category_get_by_name('Test_category').name == 'Test_category'

def test_repository_can_get_all_categories(in_memory_repo):
    categories = in_memory_repo.category_get_all()
    assert len(categories) > 1 and type(categories) is list

def test_repository_can_get_a_list_of_category_names(in_memory_repo):
    category_names = in_memory_repo.category_get_all_names()
    assert len(category_names) > 1 and type(category_names) is list and type(category_names[0]) is str


# --- Users repository methods ---
def test_repository_can_add_user_and_get_by_username(in_memory_repo):
    user = User("TestUser123", "TestUser123")
    in_memory_repo.user_add(user)

    retrieved = in_memory_repo.user_get_by_username("TestUser123")
    assert retrieved.username == "TestUser123"
    assert retrieved is user
    assert retrieved.id == 1

def test_repository_can_get_user_by_id(in_memory_repo):
    user1 = User("TestUser111", "TestUser111")
    user2 = User("TestUser222", "TestUser222")
    in_memory_repo.user_add(user1)
    in_memory_repo.user_add(user2)

    retrieved1 = in_memory_repo.user_get_by_id(user1.id)
    retrieved2 = in_memory_repo.user_get_by_id(user2.id)
    assert retrieved1.id == 1
    assert retrieved2.id == 2
    assert retrieved1.username == "TestUser111"
    assert retrieved2.username == "TestUser222"



# --- Reviews repository methods ---
def test_repository_can_add_review_and_get_by_id(in_memory_repo):
    user = User("TestUser111", "TestUser111")
    in_memory_repo.user_add(user)

    review = Review(1, 38, 3, "Test review", date.today())
    in_memory_repo.reviews_add(review)

    result = in_memory_repo.reviews_get_by_id(review.id)

    assert result.id == review.id
    assert result.recipe_id == 38
    assert result.rating == 3
    assert result.text == "Test review"
    assert result.created_date == date.today()



def test_repository_can_get_all_reviews_by_user_id_and_recipe_id(in_memory_repo):
    user = User("TestUser111", "TestUser111")
    in_memory_repo.user_add(user)
    review1 = Review(1, 38, 1, "Test review1", date.today())
    review2 = Review(1, 56, 2, "Test review2", date.today())
    review3 = Review(1, 1940, 3, "Test review3", date.today())
    in_memory_repo.reviews_add(review1)
    in_memory_repo.reviews_add(review2)
    in_memory_repo.reviews_add(review3)

    assert len(in_memory_repo.reviews_get_all_by_user_id(1)) == 3
    assert in_memory_repo.reviews_get_all_by_user_id(1)[0] is review1
    assert len(in_memory_repo.reviews_get_all_by_recipe_id(56)) == 1
    assert in_memory_repo.reviews_get_all_by_recipe_id(56)[0] is review2



# --- Favourites repository methods ---
def test_repository_can_add_and_get_favourites_by_id(in_memory_repo):
    favourite = Favourite(1, 38)

    in_memory_repo.favourite_add(favourite)

    all_favourites = in_memory_repo.favourite_get_all()
    assert len(all_favourites) == 1
    assert isinstance(all_favourites, list)

    user_favourites = in_memory_repo.favourite_get_all_by_user_id(favourite.user_id)
    assert isinstance(user_favourites, list)
    assert len(user_favourites) == 1
    assert user_favourites[0] is favourite


def test_repository_can_remove_favourite(in_memory_repo):
    favourite = Favourite(2, 38)
    in_memory_repo.favourite_add(favourite)

    in_memory_repo.favourite_remove(2, 38)
    assert len(in_memory_repo.favourite_get_all_by_user_id(2)) == 0
