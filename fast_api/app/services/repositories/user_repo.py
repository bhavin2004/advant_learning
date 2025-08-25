from fastapi import HTTPException
from sqlalchemy.orm import Session
from ...models.models import Users
from ...utils.utils import bcrypt_contest,authenticate_user

class UserRepo:
    def __init__(self,db: Session):
        self.db = db

    def get_user_details_by_user_id(self,user_id:int):
        return self.db.query(Users).filter(Users.id == user_id).first()


    def change_user_pwd(self,user_id:int,current_pwd:str,new_pwd:str):
        user = self.get_user_details_by_user_id(user_id)
        if not authenticate_user(user.username,current_pwd,self.db):
            raise HTTPException(401,"Authentocation Failed")
        user.hashed_password = bcrypt_contest.encrypt(new_pwd)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user


    def change_phone_no(self,user_id:int,phone_no:str):
        user = self.get_user_details_by_user_id(user_id)
        user.phone_number = phone_no

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user