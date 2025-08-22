import recipe.adapters.repository as repo

NUMBER_OF_FEATURE_RECIPES = 4

def get_number_of_recipes():
    return repo.repo_instance.recipe_get_quantity()

def get_latest_recipes():
    return repo.repo_instance.recipe_get_latest(NUMBER_OF_FEATURE_RECIPES)