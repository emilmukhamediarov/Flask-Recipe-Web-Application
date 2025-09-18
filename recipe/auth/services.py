from recipe.adapters.repository import AbstractRepository
from recipe.domainmodel.user import User

def retrieve_user_by_name(username, repository:AbstractRepository):
    return repository.get_user_by_username(username)

def retrieve_user_by_id(user_id, repository:AbstractRepository):
    return repository.get_user_by_id(int(user_id))

def add_new_user(new_user:User, repository:AbstractRepository):
    repository.add_user(new_user)
