from sqlalchemy.orm import Session
from ...models.models import Users
from ...utils.utils import bcrypt_contest
from ...schemas.schemas import UserRequest



def create_user(create_user_request:UserRequest,db:Session):
    user_model = Users(
                email=create_user_request.email,
                username=create_user_request.username,
                first_name=create_user_request.first_name,
                last_name=create_user_request.last_name,
                hashed_password=bcrypt_contest.hash(create_user_request.password),
                is_active=True,
                role=create_user_request.role,
                phone_number=create_user_request.phone_number
            )
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model   

def get_user_by_id(user_id:int,db:Session):
    return db.query(Users).filter(Users.id == user_id).first()


def get_user_by_email(email:str,db:Session):
    return db.query(Users).filter(Users.email == email).first()


def list_users(db:Session):
    return db.query(Users).all()


def change_user_pwd(user:Users,new_pwd:str,db:Session):
    user.hashed_password = bcrypt_contest.hash(new_pwd)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def change_phone_no(user:Users,phone_no:str,db:Session):
    user.phone_number = phone_no
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id:int,db:Session):
    user = get_user_by_id(user_id,db)
    if user:
        db.delete(user)
        db.commit()
    return user

