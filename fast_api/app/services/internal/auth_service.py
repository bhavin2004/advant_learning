from ..repositories.auth_repo import verify_user_credentials
from sqlalchemy.orm import Session

def authenticate_user_service(username:str,password:str,db:Session):
    return verify_user_credentials(username,password,db)
     
