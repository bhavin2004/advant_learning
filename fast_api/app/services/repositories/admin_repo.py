from sqlalchemy.orm import Session
from ...models.models import Todo


class AdminRepo:

    def __init__(self,db: Session):
        self.db = db

    def get_all_todo(self):
        res = self.db.query(Todo).all()
        return res


    def get_todo_by_id(self,todo_id:int):
        return self.db.query(Todo).filter(Todo.id == todo_id).first()

    def delete_todo_by_id(self,todo_id:int):
        todo = self.db.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            self.db.delete(todo)
            self.db.commit()
            return True
        return None


