from ..repositories.auth_repo import create_user
from ...schemas.schemas import UserRequest
from sqlalchemy.orm import Session

def create_user_service(create_user_request:UserRequest,db:Session):
    return create_user(create_user_request,db)