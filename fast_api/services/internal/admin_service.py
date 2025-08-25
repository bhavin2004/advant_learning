from sqlalchemy.orm import Session
from ..repositories.admin_repo import get_all_todo,get_todo_by_id,delete_todo_by_id

def get_all_todo_service(db:Session):
    return get_all_todo(db)


def get_todo_by_id_service(todo_id:int,db:Session):
    return get_todo_by_id(todo_id,db)

def delete_todo_service(todo_id:int,db:Session):
    return delete_todo_by_id(todo_id,db)