from sqlalchemy.orm import Session
from ...models.models import Todo


def get_all_todo(db:Session):
    res = db.query(Todo).all()
    return res


def get_todo_by_id(todo_id:int,db:Session):
    return db.query(Todo).filter(Todo.id == todo_id).first()
    
def delete_todo_by_id(todo_id:int,db:Session):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
