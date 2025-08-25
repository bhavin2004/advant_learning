from sqlalchemy.orm import Session
from ...models.models import Todo
from ...schemas.schemas import TodoRequest

class TodoRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_todo(self,user_id:int):
        return self.db.query(Todo).filter(Todo.owner_id == user_id).all()

    def get_todo_by_id_of_user(self,user_id:int,todo_id:int):
        return self.db.query(Todo).filter(Todo.id == todo_id).filter(Todo.owner_id == user_id).first()


    def create_todo_for_user(self,user_id:int,todo_request:TodoRequest):
       try:
           todomodel = Todo(**todo_request.model_dump(), owner_id=user_id)

           self.db.add(todomodel)
           self.db.commit()
           self.db.refresh(todomodel)
           return todomodel
       except:
           return None

    def update_todo_for_user(self,todo_model:Todo,todo_req:TodoRequest):
        todo_model.title = todo_req.title
        todo_model.description = todo_req.description
        todo_model.priority = todo_req.priority
        todo_model.complete = todo_req.complete
        self.db.add(todo_model)
        self.db.commit()
        self.db.refresh(todo_model)
        return todo_model



    def delete_todo_for_user(self,todo_id:int):
        todo = self.db.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            self.db.delete(todo)
            self.db.commit()

