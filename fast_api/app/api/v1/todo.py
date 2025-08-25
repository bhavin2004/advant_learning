from fastapi import APIRouter,Path,HTTPException,Request
from starlette import status
from starlette.responses import  RedirectResponse
from fastapi.templating import  Jinja2Templates
from ...utils.utils import user_dependency,db_config,get_current_user
from ...schemas.schemas import TodoRequest
from ...services.repositories.todo_repo import TodoRepo
router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

templates = Jinja2Templates(directory="app/templates")



def redirect_to_login():
    redirect_response = RedirectResponse(url='/auth/login-page',status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response


##Pages
@router.get("/todo-page",status_code=200)
async def render_todo_page(request: Request,db: db_config):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))
        if user is None:
            return redirect_to_login()
        todo_repo = TodoRepo(db)
        todos = todo_repo.get_todo(user.get('id'))

        return templates.TemplateResponse('todo.html',{'request':request,'todos':todos,'user':user})
    except Exception:
        return redirect_to_login()


@router.get('/add-todo-page',status_code=200)
async def add_todo_page(request: Request,db: db_config):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse('add-todo.html',{'request':request,'user':user})
    except Exception:
        return redirect_to_login()

@router.get('/edit-todo-page/{todo_id}',status_code=200)
async def edit_todo_page(request: Request,db: db_config, todo_id: int):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        if user is None:
            return redirect_to_login()
        todo_repo = TodoRepo(db)
        todo = todo_repo.get_todo_by_id_of_user(user.get('id'),todo_id)
        return templates.TemplateResponse('edit-todo.html',{'request':request,'user':user,'todo':todo})
    except Exception:
        return redirect_to_login()



## API ENDPOINTS
@router.get("/",status_code=status.HTTP_200_OK)
def read_all(db: db_config,
             user:user_dependency):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
    todo_repo = TodoRepo(db)
    res = todo_repo.get_todo(user.get('id'))
    if res:
        return res
    raise HTTPException(404,"NO RECORDS FOUND")

@router.get("/todo/{todo_id}")
def read_todo_by_id(user:user_dependency,db:db_config,todo_id:int = Path(gt=0)):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
    todo_repo = TodoRepo(db)
    todo_model = todo_repo.get_todo_by_id_of_user(user.get('id'),todo_id)
    if todo_model: 
        return todo_model
    raise HTTPException(404,"Todo Not Found.")

@router.post('/todo', status_code=status.HTTP_201_CREATED)
def create_todo(user:user_dependency,db:db_config,todo_request: TodoRequest):

    if not user:
        raise HTTPException(401,"Authentocation Failed")
    todo_repo = TodoRepo(db)
    todo_repo.create_todo_for_user(user.get("id"),todo_request)
    
@router.put('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
def update_todo(user:user_dependency,db:db_config, todo_req: TodoRequest, todo_id:int = Path(gt=0)):

    if not user:
        raise HTTPException(401,"Authentocation Failed")
    todo_repo = TodoRepo(db)
    todo_model = todo_repo.get_todo_by_id_of_user(user.get('id'),todo_id)
    if not todo_model:
        raise HTTPException(404,"Todo Not Found")
     
    todo_repo.update_todo_for_user(todo_model,todo_req)
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(user:user_dependency,
                db: db_config,todo_id : int = Path(gt=0)):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
    todo_repo = TodoRepo(db)
    todo_model = todo_repo.get_todo_by_id_of_user(user.get('id'),todo_id)
    
    if not todo_model:
        raise HTTPException(404,"Todo Not Found")
    
    todo_repo.delete_todo_for_user(todo_id)