from sqlalchemy.orm import Session
from ...models.models import Todo
from ...schemas.schemas import TodoRequest


def get_todo(user_id:int,db:Session):
    return db.query(Todo).filter(Todo.owner_id == user_id).all()


def list_all_todo(db:Session):
    return db.query(Todo).all()

def get_todo_by_id(todo_id:int,db:Session,user_id:int|None=None):
    todo = db.query(Todo).filter(Todo.id == todo_id)
    if user_id:
        todo = todo.filter(Todo.owner_id == user_id)
    return todo.first()


def create_todo(user_id:int,todo_request:TodoRequest,db:Session):
    todomodel =  Todo(**todo_request.model_dump(),owner_id = user_id)
    
    db.add(todomodel)
    db.commit()
    db.refresh(todomodel)
    return todomodel
    
def update_todo(todo_model: Todo, todo_req: TodoRequest, db: Session):
    for key, value in todo_req.model_dump(exclude_unset=True).items():
        setattr(todo_model, key, value)
    db.commit()
    db.refresh(todo_model)
    return todo_model


    
    
def delete_todo(todo_id:int,db:Session):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return None