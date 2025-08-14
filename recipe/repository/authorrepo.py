class AuthorRepo:
    def __init__(self):
        self._authors = {}

    def add(self, author):
        self._authors[author.id] = author

    def get_by_id(self, author_id):
        return self._authors.get(author_id)

    def all(self):
        return list(self._authors.values())