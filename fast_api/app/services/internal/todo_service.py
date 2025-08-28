from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repositories.todo_repo import get_todo,get_todo_by_id,create_todo,update_todo,delete_todo,list_all_todo
from ...schemas.schemas import TodoRequest


def list_user_todos(user_id: int, db: Session):
    return get_todo(user_id, db)


def list_all_todos(db: Session):
    return list_all_todo(db)


def get_todo_by_id_service( todo_id: int, db: Session,user_id: int|None=None):
    todo = get_todo_by_id(todo_id, db, user_id)
    if not todo:
        raise HTTPException(404,"Todo Not Found.")
    return todo


def create_new_todo(user_id: int, todo_request: TodoRequest, db: Session):
    return create_todo(user_id, todo_request, db)


def update_existing_todo(user_id: int, todo_id: int, todo_req: TodoRequest, db: Session):
    todo = get_todo_by_id_service(todo_id, db, user_id)
    if not todo:
        raise HTTPException(404,"Todo Not Found.")
    return update_todo(todo, todo_req, db)


def delete_todo_service(todo_id: int, db: Session):

    delete_todo(todo_id, db)
    return {"message": "Todo deleted successfully"}


