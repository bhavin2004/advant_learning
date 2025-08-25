from ...models.models import Users
from ...schemas.schemas import UserRequest
from sqlalchemy.orm import Session
from ...utils.utils import bcrypt_contest


class AuthRepo:
    def __init__(self,db: Session):
        self.db = db

    def create_user(self,create_user_request:UserRequest):
        try:
            create_user_model = Users(
                email=create_user_request.email,
                username=create_user_request.username,
                first_name=create_user_request.first_name,
                last_name=create_user_request.last_name,
                hashed_password=bcrypt_contest.hash(create_user_request.password),
                is_active=True,
                role=create_user_request.role,
                phone_number=create_user_request.phone_number
            )
            self.db.add(create_user_model)
            self.db.commit()
            self.db.refresh(create_user_model)
            return create_user_request
        except:
            return None