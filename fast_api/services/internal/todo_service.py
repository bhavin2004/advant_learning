from sqlalchemy.orm import Session
from ...schemas.schemas import TodoRequest
from ...services.repositories.todo_repo import get_todo,get_todo_by_id_of_user,create_todo_for_user,update_todo_for_user,delete_todo_for_user


def list_todos_service(user_id:int, db: Session):
    return get_todo(user_id, db)


def get_todo_for_user_service(user_id:int, todo_id: int, db: Session):
    todo = get_todo_by_id_of_user(user_id, todo_id, db)
    return todo


def create_todo_service(user_id: int, todo_req: TodoRequest, db: Session):
    return create_todo_for_user(user_id, todo_req, db)


def update_todo_service(user_id:int, todo_id: int, todo_req: TodoRequest, db: Session):
    todo = get_todo_for_user_service(user_id, todo_id, db)
    return update_todo_for_user(todo, todo_req, db)


def delete_todo_service(user_id:int, todo_id: int, db: Session):
    return delete_todo_for_user(todo_id, db)
    