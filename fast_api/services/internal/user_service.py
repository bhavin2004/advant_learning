from ..repositories.user_repo import get_user_details_by_user_id,change_user_pwd,change_phone_no
from sqlalchemy.orm import Session
from fastapi import HTTPException
from ...utils.utils import authenticate_user


def get_user_detail_service(user_id:int,db:Session):
    return get_user_details_by_user_id(user_id,db)



def change_password_service(user_id:int,current_pwd:str,new_pwd:str,db:Session):
    user = get_user_detail_service(user_id,db)
    user = authenticate_user(user.username,current_pwd,db)
    
    if not user:
        raise HTTPException(401,"Wrong Current Password")
    
    return change_user_pwd(user,new_pwd,db)


def change_phone_number_service(user_id:int,phone_no:str,db:Session):
    user_model = get_user_detail_service(user_id,db)
    if not user_model:
        raise HTTPException(404,"NO RECORDS FOUND")
    
    return change_phone_no(user_model,phone_no,db)