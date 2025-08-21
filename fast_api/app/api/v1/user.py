from fastapi import APIRouter,Path,HTTPException
from ....models.models import Users
from starlette import status
from ....utils.utils import user_dependency,db_config,authenticate_user,bcrypt_contest
from ....schemas.schemas import UserPasswordRequest

 

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get('/',status_code=status.HTTP_200_OK)
def get_user_details(user:user_dependency,db:db_config):
    if not user:
        raise HTTPException(401,"Authentocation Failed")    
    
    res = db.query(Users).filter(Users.id == user['id']).first()
    if res:
        return res
    raise HTTPException(404,"NO RECORDS FOUND")

@router.put("/change_password",status_code=status.HTTP_204_NO_CONTENT)
def change_password(user:user_dependency,db:db_config,password_request:UserPasswordRequest):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
    
    res = db.query(Users).filter(Users.id == user['id']).first()
    user = authenticate_user(res.username,password_request.current_pwd,db)
    
    if not user:
        raise HTTPException(401,"Wrong Current Password")
    
    user.hashed_password= bcrypt_contest.hash(password_request.new_pwd)
    db.add(user)
    db.commit()
        
    # raise HTTPException(404,"NO RECORDS FOUND")
    
@router.put('/change_phone_number/{phone_no}',status_code=status.HTTP_204_NO_CONTENT)
def change_phone_number(user:user_dependency,db:db_config,phone_no:str = Path(min_length=10,max_length=10)):

    if not user:
        raise HTTPException(401,"Authentocation Failed")
    
    user_model = db.query(Users).filter(Users.id == user['id']).first()
    if not user_model:
        raise HTTPException(404,"NO RECORDS FOUND")
    
    user_model.phone_number = phone_no
    
    db.add(user_model)
    db.commit()