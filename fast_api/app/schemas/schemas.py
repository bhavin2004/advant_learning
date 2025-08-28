from pydantic import BaseModel,Field

class UserRequest(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str = Field(min_length=10,max_length=10,default='1234567890')
    
class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str = Field(min_length=3,max_length=100)
    priority:int = Field(gt=0,lt=6)
    complete: bool = Field(default=False)
    
class UserPasswordRequest(BaseModel):
    current_pwd:str
    new_pwd:str = Field(min_length=8)