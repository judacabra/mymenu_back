from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import User, Profile
import os


class UserService:
    def __init__(self, db: Session):
        self.db = db


    def get_user_db(self, email: str, username: str = None):
        try:
            db_user = self.db.query(User).filter(or_(User.username == username, User.email == email)).first()

            if db_user:
                if db_user.username == username:
                    return {"message": "Username already registered", "id": db_user.id}
                elif db_user.email == email:
                    return {"message": "Email already registered", "id": db_user.id}

            return {"message": "Username and email are available", "id": 0}

        except SQLAlchemyError as e:
            print(f"Error getting user: {e}")
            self.db.rollback()
            return False


    def verify_user_state(self, user_id: int):
        try:
            db_user = self.db.query(User).get(user_id)

            if db_user:
                if db_user.active:
                    return "User is already active"
                else:
                    return "User is already inactive"

            return False

        except SQLAlchemyError as e:
            print(f"Error verifying user state: {e}")
            self.db.rollback()
            return False


    def register_user_db(self, user):
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user

        except SQLAlchemyError as e:
            print(f"Error adding user: {e}")
            self.db.rollback()
            return False


    def modify_user_db(self, user: dict):
        try:
            db_user = self.db.query(User).get(user.id)

            if not db_user:
                return False

            for key in [
                'id_profile', 'active', 'name',
                'username', 'email', 'password'
            ]:
                if getattr(user, key) is not None:
                    setattr(db_user, key, getattr(user, key))

            self.db.commit()
            self.db.refresh(db_user)
            return db_user

        except SQLAlchemyError as e:
            print(f"Error modifying user: {e}")
            self.db.rollback()
            return False

        try:
            query = self.db.query(User)
            db_user = query.filter(User.id == id).first()

            if db_user:
                if filename is not None:
                    db_user.picture = filename

                self.db.commit()
                self.db.refresh(db_user)
                return {"message": "Profile picture chnaged succesfully"}

            raise ValueError("User not found")

        except SQLAlchemyError as e:
            print(f"Error adding the file: {e}")
            self.db.rollback()
            return False
