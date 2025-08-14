class CategoryRepo:
    def __init__(self):
        self._categories = {}

    def add(self, category):
        self._categories[category.name] = category

    def get_by_name(self, category_name):
        return self._categories.get(category_name)

    def all(self):
        return list(self._categories.values())