class RecipeImage:
    id_count = 1
    def __init__(self, recipe_id: int, url: str, id: int | None = None):
        if id is None:
            self.__id = RecipeImage.id_count
            RecipeImage.id_count += 1
        else:
            self.__id = id
        self.__recipe_id = recipe_id
        self.__url = url
        RecipeImage.id_count += 1

    def __repr__(self) -> str:
        return f"{self.url}"

    def __str__(self) -> str:
        return f"{self.url}"

    def __eq__(self, other):
        if not isinstance(other, RecipeImage):
            return False
        return self.recipe_id == other.recipe_id and self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, RecipeImage):
            return NotImplemented
        return self.id < other.id

    def __hash__(self):
        return hash((self.recipe_id, self.id))

    @property
    def id(self) -> int:
        return self.__id

    @property
    def recipe_id(self) -> int:
        return self.__recipe_id

    @property
    def url(self) -> str:
        return self.__url
