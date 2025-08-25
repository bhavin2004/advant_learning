from sqlalchemy.orm import Session
from ...models.models import Todo
from ...schemas.schemas import TodoRequest


def get_todo(user_id:int,db:Session):
    return db.query(Todo).filter(Todo.owner_id == user_id).all()

def get_todo_by_id_of_user(user_id:int,todo_id:int,db:Session):
    return db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user_id).first()


def create_todo_for_user(user_id:int,todo_request:TodoRequest,db:Session):
    todomodel =  Todo(**todo_request.model_dump(),owner_id = user_id)
    
    db.add(todomodel)
    db.commit()
    db.refresh(todomodel)
    return todomodel
    
def update_todo_for_user(todo_model:Todo,todo_req:TodoRequest,db:Session):
    todo_model.title = todo_req.title
    todo_model.description = todo_req.description
    todo_model.priority = todo_req.priority
    todo_model.complete = todo_req.complete
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model

    
    
def delete_todo_for_user(todo_id:int,db:Session):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
