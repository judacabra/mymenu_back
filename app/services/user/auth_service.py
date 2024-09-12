from datetime import datetime, timedelta, timezone
from jose import jwt
from typing import Optional
from passlib.context import CryptContext
import bcrypt

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    def __init__(self, db: Session):
        self.db = db
        

    def verify_user(self, username: str):
        try:
            user = self.db.query(User).filter(User.username == username).first()

            if not user:
                return {"message": "User not found", "active": False, "password": None, "username": None}

            if not user.active:
                return {"message": "User is not active", "active": False, "password": None, "username": None}

            return {"message": "User found", "active": True, "password": user.password, "username": user.username, "id": user.id}

        except SQLAlchemyError as e:
            print(f"Error verifying user: {e}")
            self.db.rollback()
            return {"message": "Error verifying user", "active": False, "password": None, "username": None}


    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)


    def hash_password(self, password: str):
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')
    

    def authenticate_user(self, username: str, password: str):
        user_info = self.verify_user(username)

        if not user_info["active"]:
            return user_info

        if not self.verify_password(password, user_info["password"]):
            return {"message": "Invalid password"}

        return user_info


    def create_access_token(self, data: dict, secret_key: str, algorithm: str, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
        return encoded_jwt
