from abc import ABC
from typing import List, Type


from sqlalchemy import func
from sqlalchemy.orm import scoped_session
from unicodedata import category

from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.user import User
from recipe.domainmodel.review import Review
from recipe.domainmodel.favourite import Favourite


# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self) -> object:
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def author_add(self, author) -> None:
        """Adds an Author to the repository
            Replaced by add_multiple
        """
        pass

    def author_get_by_name(self, author_name) -> Author:
        """Returns an Author by their name
            Replaced by get_by_id
        """
        pass

    def author_get_by_id(self, author_id: int) -> Author:
        """Returns the User by id"""
        with self._session_cm as scm:
            return scm.session.query(Author).filter(Author._Author__id == author_id).first()

    def author_get_all(self) -> List[Author]:
        """Returns a list of Authors
            Not used in implementation
        """
        pass

    def author_get_all_names(self) -> List[property]:
        """Returns a list of Author names"""
        authors = self._session_cm.session.query(Author).all()
        return [a.name for a in authors]


    def category_add(self, category) -> None:
        """Adds a Category to the repository
            Replaced by add_multiple
        """
        pass

    def category_get_by_name(self, category_name) -> Category:
        """Returns a Category by its name
            Replaced by get_by_id
        """
        pass

    def category_add_by_name(self, category_name) -> Category:
        """Creates a new Category with the given name and returns the new object
            Replaced by add_multiple
        """
        pass

    def category_get_all(self) -> List[Category]:
        """Returns a list of Categories
            Not used in implementation
        """
        pass

    def category_get_all_names(self) -> List[property]:
        """Returns a list of Category Names"""
        categories = self._session_cm.session.query(Category).all()
        return [c.name for c in categories]

    def recipe_add(self, recipe) -> None:
        """Adds a Recipe to the repository
        Replaced by add_multiple
        """
        pass

    def recipe_get_by_name(self, recipe_name) -> Recipe:
        """Returns a Recipe by its name
        Not used in implementation"""
        pass

    def recipe_get_all(self) -> List[Recipe]:
        """Returns a list of Recipes"""
        return self._session_cm.session.query(Recipe).all()


    def recipes_get_all_by_category(self, category_name) -> List[Recipe]:
        """Returns a list of Recipes by category
        Not used in implementation
        """
        pass

    def recipe_get_by_id(self, recipe_id: int) -> Recipe | None:
        with self._session_cm as scm:
            return scm.session.query(Recipe).filter(Recipe._Recipe__id == recipe_id).first()

    def recipe_get_quantity(self) -> int:
        return self._session_cm.session.query(Recipe).count()

    def recipe_get_random(self) -> Type[Recipe]:
        return self._session_cm.session.query(Recipe).order_by(func.random()).first()

    def recipe_get_latest(self, num: int):
        return self._session_cm.session.query(Recipe).order_by(Recipe._Recipe__id.desc()).limit(num).all()

    def user_add(self, user: User) -> None:
        """Adds User to the dictionary"""
        with self._session_cm as scm:
            existing = scm.session.query(User).filter(User._User__username == user.username).first()
            if existing is not None:
                raise ValueError(f"Username '{user.username}' already exists")
            scm.session.add(user)
            scm.session.commit()

    def user_get_by_username(self, username: str) -> User:
        """Returns the User by username"""
        with self._session_cm as scm:
            return scm.session.query(User).filter(User._User__username == username).first()

    def user_get_by_id(self, user_id: int) -> User:
        """Returns the User by id"""
        with self._session_cm as scm:
            return scm.session.query(User).filter(User._User__id == user_id).first()

    def reviews_add(self, review) -> None:
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")

        with self._session_cm as scm:
            scm.session.add(review)

            scm.commit()

    def reviews_remove(self, review) -> None:
        if not isinstance(review, Review):
            raise TypeError("Expected a Review instance.")

        with self._session_cm as scm:
            to_delete = scm.session.query(Review).filter(Review._Review__id == review.id).first()
            if to_delete is not None:
                scm.session.delete(to_delete)
                scm.commit()

    def reviews_get_by_id(self, review_id: int) -> Review:
        with self._session_cm as scm:
            return scm.session.query(Review).filter(Review._Review__id == review_id).first()

    def reviews_get_all_by_user_id(self, user_id: int) -> List[Review]:
        with self._session_cm as scm:
            return scm.session.query(Review).filter(Review._Review__user_id == user_id).all()

    def reviews_get_all_by_recipe_id(self, recipe_id: int) -> List[Review]:
        with self._session_cm as scm:
            return scm.session.query(Review).filter(Review._Review__recipe_id == recipe_id).all()

    def favourite_add(self, favourite) -> None:
        """Adds a recipe to favourites"""
        with self._session_cm as scm:

            existing = scm.session.query(Favourite).filter_by(user_id=favourite.user_id,recipe_id=favourite.recipe_id).first()

            if existing is None:
                scm.session.add(favourite)
                scm.commit()

    def favourite_remove(self, user_id, recipe_id) -> None:
        """Removes a favourite by id match"""
        with self._session_cm as scm:
            favourites = scm.session.query(Favourite).filter(Favourite._Favourite__user_id == user_id, Favourite._Favourite__recipe_id == recipe_id).all()

            for f in favourites:
                scm.session.delete(f)

            scm.commit()

    def favourite_get_all(self) -> List[Favourite]:
        """Returns a list of favourites"""
        pass

    def favourite_get_all_by_user_id(self, user_id) -> List[Favourite]:
        """Returns a list of favourites by user_id"""
        with self._session_cm as scm:
            query = scm.session.query(Favourite).filter(Favourite._Favourite__user_id == user_id)

            return query.all()

    def add_multiple_recipes(self, recipes: List[Recipe]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for recipe in recipes:
                    scm.session.add(recipe)
            scm.commit()

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    scm.session.add(author)
            scm.commit()

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()