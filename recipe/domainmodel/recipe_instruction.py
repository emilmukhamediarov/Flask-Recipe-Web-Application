class RecipeInstruction:
    def __init__(self, recipe_id: int, step: str):
        self.__recipe_id = recipe_id
        self.__step = step


    def __repr__(self) -> str:
        return f"{self.step}"

    def __eq__(self, other):
        if not isinstance(other, RecipeInstruction):
            return False
        return self.recipe_id == other.recipe_id

    def __lt__(self, other):
        if not isinstance(other, RecipeInstruction):
            return NotImplemented
        return self.recipe_id < other.recipe_id

    def __hash__(self):
        return hash(self.recipe_id)

    @property
    def recipe_id(self) -> int:
        return self.__recipe_id

    @property
    def step(self) -> str:
        return self.__step


