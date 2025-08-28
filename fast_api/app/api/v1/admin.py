from fastapi import APIRouter,Path,HTTPException
from starlette import status
from ...services.internal.todo_service import list_all_todos,get_todo_by_id_service,delete_todo_service
from ...utils.utils import user_dependency,db_config
 

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)



@router.get('/todos',status_code=status.HTTP_200_OK)
def get_all_todos(user:user_dependency,db:db_config):
    if not user or user['role'] != 'admin':
        raise HTTPException(401,"Authentocation Failed")
    
    res = list_all_todos(db)
    if res:
        return res
    raise HTTPException(404,"NO RECORDS FOUND")

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependency,
                db: db_config,todo_id : int = Path(gt=0)):
    if not user or user['role'] != 'admin':
        raise HTTPException(401,"Authentocation Failed")
 
    todo_model = get_todo_by_id_service(todo_id,db)
    
    if not todo_model:
        raise HTTPException(404,"Todo Not Found")
    delete_todo_service(todo_id,db)