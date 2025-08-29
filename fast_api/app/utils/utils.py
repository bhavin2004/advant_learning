from fastapi.security import OAuth2PasswordBearer
from ..core.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends,HTTPException, Request
from passlib.context import CryptContext
from ..models.models import Users
from datetime import timezone,datetime,timedelta
from jose import jwt,JWTError
from dotenv import load_dotenv
import os

def connect_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGO = os.getenv('ALGO')

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


bcrypt_contest = CryptContext(schemes=['bcrypt'],deprecated='auto')



def create_access_token(username: str, user_id: int, role: str, expire_delta: int):
    expire_delta: timedelta = timedelta(minutes=expire_delta)
    encode = {
        'sub': username,
        'id': user_id,
        'role': role
    }

    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, ALGO)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGO)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')

        if username is None or user_id is None:
            raise HTTPException(401, "Could not validate user.")
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(401, "Could not validate user.")

def get_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGO)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')

        if username is None or user_id is None:
            return None
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        return None



db_config = Annotated[Session,Depends(connect_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]
user_config = Annotated[dict,Depends(get_user)]


def authenticate_user(username: str,pwd:str, db:db_config):
    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        return False
    if not bcrypt_contest.verify(pwd, user.hashed_password):
        return False
    return user
