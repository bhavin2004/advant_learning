from ...models.models import Users
from ...schemas.schemas import UserRequest
from sqlalchemy.orm import Session
from ...utils.utils import bcrypt_contest

def create_user(create_user_request:UserRequest,db:Session):
    create_user_model = Users(
        email = create_user_request.email,
        username = create_user_request.username,
          first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_contest.hash(create_user_request   .password),
        is_active = True,
        role = create_user_request.role,
        phone_number = create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return create_user_request