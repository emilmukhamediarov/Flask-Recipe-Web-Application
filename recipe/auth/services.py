from recipe.adapters.repository import AbstractRepository

def retrieve_user_by_name(username, repository:AbstractRepository):
    return repository.get_user_by_username(username)

def retrieve_user_by_id(user_id, repository:AbstractRepository):
    return repository.get_user_by_id(int(user_id))