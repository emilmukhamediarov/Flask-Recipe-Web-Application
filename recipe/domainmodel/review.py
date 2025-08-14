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
        if value < 0 or value > 5:
            raise ValueError("rating must be between 0 and 5 inclusive.")
        self.__rating = value

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value: str):
        self.__text = value

    def __repr__(self):
        return f"Review(id={self.id}, rating={self.rating}, author={getattr(self.author, 'id') }, recipe={getattr(self.recipe, 'id')}, text={self.text})"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return self.__id == other.id

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        return self.__rating < other.rating
