from fastapi import APIRouter,Depends,HTTPException,Request
from ....schemas.schemas import UserRequest
from ....models.models import Users
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from ....utils.utils import db_config,bcrypt_contest,authenticate_user,create_access_token,get_current_user


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGO = os.getenv('ALGO')




templates = Jinja2Templates(directory="fast_api/templates")


@router.post('/',status_code=status.HTTP_201_CREATED)
def create_user(create_user_request: UserRequest,
                db: db_config):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
          first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_contest.hash(create_user_request   .password),
        is_active = True,
        role = create_user_request.role,
        phone_number = create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()
    
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

