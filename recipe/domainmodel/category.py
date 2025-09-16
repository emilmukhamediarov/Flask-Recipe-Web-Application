from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from recipe.domainmodel.recipe import Recipe

class Category:
    id_count = 1
    def __init__(self, name: str, recipes: List["Recipe"] = None):
        self.__name = name
        self.__id = Category.id_count
        Category.id_count += 1
        self.__recipes = recipes if recipes is not None else []

    def __repr__(self) -> str:
        return f"<Category: {self.name}>"

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
    def recipes(self) -> List["Recipe"]:
        return self.__recipes

    def add_recipe(self, recipe: "Recipe") -> None:
        from recipe.domainmodel.recipe import Recipe
        if not isinstance(recipe, Recipe):
            raise TypeError("Expected a Recipe instance")
        if recipe not in self.__recipes:
            self.__recipes.append(recipe)

