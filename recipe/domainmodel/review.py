class Review:
    id_count = 1
    def __init__(self, user_id: int, recipe_id: int, rating: int, text: str):
        self.__user_id = user_id
        self.__recipe_id = recipe_id
        self.__rating = rating
        if self.__rating < 0 or self.__rating > 5:
            raise ValueError("rating must be between 0 and 5 inclusive.")
        self.__text = text
        self.__id = Review.id_count
        Review.id_count += 1


    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def recipe_id(self):
        return self.__recipe_id

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
        return self.__id < other.id
