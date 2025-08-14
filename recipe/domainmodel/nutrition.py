class Nutrition:
# TODO: Complete the implementation of the Nutrition class.
    id_count = 0
    def __init__(self, data: object):

        self.__data = data
        self.__id = Nutrition.id_count
        Nutrition.id_count += 1

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value