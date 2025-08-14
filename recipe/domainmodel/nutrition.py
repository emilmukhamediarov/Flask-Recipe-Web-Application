class Nutrition:
# TODO: Complete the implementation of the Nutrition class.
    id_count = 0
    def __init__(self, nutrition: object):

        self.__nutrition = nutrition
        self.__id = Nutrition.id_count
        Nutrition.id_count += 1

    @property
    def nutrition(self):
        return self.__nutrition