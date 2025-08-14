class Favourite:
# TODO: Complete the implementation of the Favourite class.
    id_count = 1
    def __init__(self, my_user: object, my_recipe: object):
        self.__user = my_user
        self.__recipe = my_recipe
        self.__id = Favourite.id_count
        Favourite.id_count += 1

    @property
    def id(self):
        return self.__id

    @property
    def user(self):
        return self.__user
    @property
    def recipe(self):
        return self.__recipe

    def __repr__(self):
        return f"favourite(id={self.id}, user={self.user}, recipe={self.recipe})"

    def __eq__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__id == other.id

    def __lt__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__id < other.id

