import recipe.adapters.repository as repo

def get_recipe(id : int):
    return repo.repo_instance.recipe_get_by_id(id)