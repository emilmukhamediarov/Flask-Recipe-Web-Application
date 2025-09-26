class Favourite:
    id_count = 1
    def __init__(self, user_id : int, my_recipe_id: int):
        self.__user_id = user_id
        self.__recipe_id = my_recipe_id
        self.__id = Favourite.id_count
        Favourite.id_count += 1

    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id
    @property
    def recipe_id(self):
        return self.__recipe_id

    def __repr__(self):
        return f"favourite(id={self.__id}, user={self.__user_id}, recipe={self.__recipe_id})"

    def __eq__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__id == other.id

    def __lt__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__id < other.id

