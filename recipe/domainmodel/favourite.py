class Favourite:
# TODO: Complete the implementation of the Favourite class.
    id_count = 1
    def __init__(self, my_user: object, my_recipe: object):
        self.__my_user = my_user
        self.__my_recipe = my_recipe
        self.__id = Favourite.id_count
        Favourite.id_count += 1

    @property
    def id(self):
        return self.__id

    @property
    def my_user(self):
        return self.__my_user
    @property
    def my_recipe(self):
        return self.__my_recipe

    def __repr__(self):
        return f"favourite(id={self.id}, recipe={self.my_recipe})"

    def __eq__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__id == other.id

    def __lt__(self, other):
        if not isinstance(other, Favourite):
            return False
        return self.__id < other.id

