from ...models.models import Users
from sqlalchemy.orm import Session
from ...utils.utils import bcrypt_contest


def get_user_by_username(username: str, db: Session):
    return db.query(Users).filter(Users.username == username).first()

def verify_user_credentials(username: str, password: str, db: Session):
    user = get_user_by_username(username, db)
    if user and bcrypt_contest.verify(password, user.hashed_password):
        return user
    return None
