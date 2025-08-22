from recipe.domainmodel.recipe import Recipe

class Category:

    def __init__(self, name: str, recipes: list[Recipe] = None):
        self.__name = name
        self.__recipes = recipes if recipes is not None else []

    def __repr__(self) -> str:
        return f"<Category {self.id}: {self.name}>"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Category):
            return False
        return self.__name == other.name

    def __lt__(self, other) -> bool:
        if not isinstance(other, Category):
            raise TypeError("Comparison must be between Category instances")
        return self.__name < other.name

    def __hash__(self) -> int:
        return hash(self.__name)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def recipes(self) -> list[Recipe]:
        return self.__recipes

    def add_recipe(self, recipe: Recipe) -> None:
        if isinstance(recipe, Recipe):
            self.__recipes.append(recipe)
        else:
            raise TypeError("Expected a Recipe instance")
