from fastapi import APIRouter,Path,HTTPException
from ....models.models import Todo
from starlette import status
from ....utils.utils import user_dependency,db_config
 

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)



@router.get('/todos',status_code=status.HTTP_200_OK)
def get_all_todos(user:user_dependency,db:db_config):
    if not user or user['role'] != 'admin':
        raise HTTPException(401,"Authentocation Failed")
    
    res = db.query(Todo).all()
    if res:
        return res
    raise HTTPException(404,"NO RECORDS FOUND")

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependency,
                db: db_config,todo_id : int = Path(gt=0)):
    if not user or user['role'] != 'admin':
        raise HTTPException(401,"Authentocation Failed")
 
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo_model:
        raise HTTPException(404,"Todo Not Found")
    print(db.query(Todo).filter(Todo.id == todo_id).delete())
    
    db.commit()