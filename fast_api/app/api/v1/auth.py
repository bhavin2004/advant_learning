from fastapi import APIRouter,Depends,HTTPException,Request
from ...schemas.schemas import UserRequest
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from ...utils.utils import db_config,bcrypt_contest,authenticate_user,create_access_token
from ...services.internal.user_service import create_user_service

# asdkaposdk

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGO = os.getenv('ALGO')




templates = Jinja2Templates(directory="app/templates")


@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: UserRequest,
                db: db_config):
    auth_repo = AuthRepo(db)
    if not auth_repo.create_user(create_user_request):
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
        
    
    # return create_user_model

@router.get('/login-page',status_code=200)
def get_login_page(request: Request):
    return (templates.TemplateResponse('login.html',{'request':request}))


@router.get('/register-page',status_code=200)
def render_register_page(request: Request):
    return templates.TemplateResponse('register.html',{'request':request})
@router.post("/token",status_code=status.HTTP_201_CREATED)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                           db:db_config):
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(401,"Could not validate User.")
    token = create_access_token(user.username,user.id,user.role,20)
    return {"access_token": token, "token_type": "bearer"}

