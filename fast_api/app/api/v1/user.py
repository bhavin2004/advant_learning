from fastapi import APIRouter,Path,HTTPException
from starlette import status
from ...utils.utils import user_dependency,db_config
from ...schemas.schemas import UserPasswordRequest
from ...services.repositories.user_repo import UserRepo
 

router = APIRouter(
    prefix='/user',
    tags=['user']
)


@router.get('/',status_code=status.HTTP_200_OK)
def get_user_details(user:user_dependency,db:db_config):
    if not user:
        raise HTTPException(401,"Authentocation Failed")    
    user_repo = UserRepo(db)
    res = user_repo.get_user_details_by_user_id(user.get("id"))
    if res:
        return res
    raise HTTPException(404,"NO RECORDS FOUND")

@router.put("/change_password",status_code=status.HTTP_204_NO_CONTENT)
def change_password(user:user_dependency,db:db_config,password_request:UserPasswordRequest):
    if not user:
        raise HTTPException(401,"Authentocation Failed")
    user_repo = UserRepo(db)
    res = user_repo.change_user_pwd(user.get('id'),password_request.current_pwd,password_request.new_pwd)
    if not res:
        raise HTTPException(404,"NO RECORDS FOUND")
        
    # raise HTTPException(404,"NO RECORDS FOUND")
    
@router.put('/change_phone_number/{phone_no}',status_code=status.HTTP_204_NO_CONTENT)
def change_phone_number(user:user_dependency,db:db_config,phone_no:str = Path(min_length=10,max_length=10)):

    if not user:
        raise HTTPException(401,"Authentocation Failed")
    user_repo = UserRepo(db)

    res = user_repo.change_phone_no(user.get('id'),phone_no)
    if not res:
        raise HTTPException(404,"NO RECORDS FOUND")