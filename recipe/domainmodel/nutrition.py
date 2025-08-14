class Nutrition:
# TODO: Complete the implementation of the Nutrition class.
    id_count = 1
    def __init__(self, data: object):

        self.__data = data
        self.__id = Nutrition.id_count
        Nutrition.id_count += 1

    @property
    def id(self):
        return self.__id

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value


    def __repr__(self):
        return f"Nutrition(id={self.id}, data={self.data})"

    def __eq__(self, other):
        if not isinstance(other, Nutrition):
            return False
        return self.__id == other.id

    def __lt__(self, other):
        if not isinstance(other, Nutrition):
            return False
        return self.__id < other.__id