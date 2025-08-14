class Review:
# TODO: Complete the implementation of the Review class.
    id_count = 0
    def __init__(self, my_author: object, my_recipe: object, rating: int, text: str):
        self.__my_author = my_author
        self.__my_recipe = my_recipe
        self.__rating = rating
        self.__text = text
        self.__id = Review.id_count
        Review.id_count += 1


    @property
    def id(self):
        return self.__id

    @property
    def author(self):
        return self.__my_author

    @property
    def recipe(self):
        return self.__my_recipe

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value: int):
        self.__rating = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value: str):
        self.__text = value