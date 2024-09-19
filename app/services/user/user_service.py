from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.models import Company, Permission, Profile, ProfilePermission, User


class UserService:
    def __init__(self, db: Session):
        self.db = db


    def consult_users_db(self):
        try:
            db_users = self.db.query(User, Company, Profile)\
            .join(Company, User.id_company == Company.id)\
            .join(Profile, User.id_profile == Profile.id)\
            .all()
        
            if db_users:
                return [
                    {
                        "id": user.id,
                        "name": user.name,
                        "username": user.username,
                        "email": user.email,
                        "active": user.active,
                        "profile_name": profile.name,
                        "company_name": company.name,
                        "fecha_creacion": user.fecha_creacion,
                    }
                    for user, company, profile in db_users
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Users: {e}")
            self.db.rollback()
            return False


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


    def get_logged_permissions_db(self, user_id: int):
        try:
            db_permissions = self.db.query(User, Profile, ProfilePermission, Permission)\
                .join(Profile, User.id_profile == Profile.id)\
                .join(ProfilePermission, Profile.id == ProfilePermission.id_profile)\
                .join(Permission, ProfilePermission.id_permission == Permission.id)\
                .filter(User.id == user_id)\
                .all()

            if db_permissions:
                return [
                    {
                        "id": permission.id,
                        "name": permission.name,
                    }
                    for user, profile, profile_permission, permission in db_permissions
                ]

        except SQLAlchemyError as e:
            print(f"Error getting logged user permissions: {e}")
            self.db.rollback()
            return False


    def get_logged_user_db(self, username: str):
        try:
            db_user = self.db.query(User, Company, Profile)\
                .join(Company, User.id_company == Company.id)\
                .join(Profile, User.id_profile == Profile.id)\
                .filter(User.username == username)\
                .first()  

            if db_user:
                user, company, profile = db_user
                db_permissions = self.get_logged_permissions_db(user.id)

                return {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "profile_name": profile.name,
                    "company_name": company.name,
                    "permissions": db_permissions or []
                }

        except SQLAlchemyError as e:
            print(f"Error getting logged user info: {e}")
            self.db.rollback()
            return False
