from sqlalchemy.orm import Session
from ...models.models import Users
from ...utils.utils import bcrypt_contest


def get_user_details_by_user_id(user_id:int,db:Session):
    return db.query(Users).filter(Users.id == user_id).first()


def change_user_pwd(user:Users,new_pwd:str,db:Session):
    user.hashed_password = bcrypt_contest.encrypt(new_pwd)
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