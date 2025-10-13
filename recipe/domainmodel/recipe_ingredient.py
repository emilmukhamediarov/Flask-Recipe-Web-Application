class RecipeIngredient:
    id_count = 1
    def __init__(self, recipe_id: int, quantity: str, ingredient: str, id: int | None = None):
        if id is None:
            self.__id = RecipeIngredient.id_count
            RecipeIngredient.id_count += 1
        else:
            self.__id = id
        self.__recipe_id = recipe_id
        self.__quantity = quantity
        self.__ingredient = ingredient

    def __repr__(self) -> str:
        return f"<RecipeIngredient: Recipe {self.recipe_id}, Position {self.position}, {self.quantity} {self.ingredient}>"

    def __eq__(self, other):
        if not isinstance(other, RecipeIngredient):
            return False
        return self.recipe_id == other.recipe_id and self.__id == other.__id

    def __lt__(self, other):
        if not isinstance(other, RecipeIngredient):
            return NotImplemented
        return self.__id < other.__id

    def __hash__(self):
        return hash((self.__recipe_id, self.__id))

    @property
    def id(self) -> int:
        return self.__id

    @property
    def recipe_id(self) -> int:
        return self.__recipe_id

    @property
    def quantity(self) -> str:
        return self.__quantity

    @property
    def ingredient(self) -> str:
        return self.__ingredient


