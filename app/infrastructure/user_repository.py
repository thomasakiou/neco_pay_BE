from sqlalchemy.orm import Session
from typing import Optional
from app.domain.user import User
from app.infrastructure.models import UserModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> Optional[User]:
        db_user = self.db.query(UserModel).filter(UserModel.username == username).first()
        return db_user.to_entity() if db_user else None

    def save(self, user: User) -> User:
        db_user = UserModel.from_entity(user)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user.to_entity()

    def exists(self, username: str) -> bool:
        return self.db.query(UserModel).filter(UserModel.username == username).first() is not None
