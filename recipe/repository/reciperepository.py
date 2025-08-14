class RecipeRepository:
    def __init__(self):
        self._recipes = {}

    def add(self, recipe):
        self._recipes[recipe.id] = recipe

    def get_by_id(self, recipe_id):
        return self._recipes.get(recipe_id)

    def all(self):
        return list(self._recipes.values())
