from datetime import datetime

from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.schemas import UserCreate, UserUpdate
from app.models.models import Company, Headquarter, Permission, Profile, ProfilePermission, User
from app.services.user.auth_service import AuthService
from app.utils.config import get_settings

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()


    def consult_users_db(self, user_id: int):
        try:
            db_user = self.db.query(User, Profile)\
                .join(Profile, User.id_profile == Profile.id)\
                .filter(User.id == user_id)\
                .first() 
            
            if db_user:
                user, profile = db_user
                
                if profile.id == 1:
                    db_users = self.consult_users_by_superadmin()
                else:
                    db_users = self.consult_users_by_headquarter(user_id)

                return db_users
        

        except SQLAlchemyError as e:
            print(f"Error getting Users: {e}")
            self.db.rollback()
            return False
    

    def consult_users_by_superadmin(self):
        try:
            db_users = self.db.query(User, Headquarter, Profile, Company)\
            .join(Headquarter, User.id_headquarter == Headquarter.id)\
            .join(Profile, User.id_profile == Profile.id)\
            .join(Company, Headquarter.id_company == Company.id)\
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
                        "headquarter_name": headquarter.name,
                        "company_name": company.name,
                        "date": user.date,
                    }
                    for user, headquarter, profile, company in db_users
                ]
        
        except SQLAlchemyError as e:
            print(f"Error getting Users by superadmin: {e}")
            self.db.rollback()
            return False


    def consult_users_by_headquarter(self, user_id: int):
        try:
            db_users = self.db.query(User, Company, Headquarter, Profile)\
                .join(User, User.id_headquarter == Headquarter.id)\
                .join(Company, Company.id == Headquarter.id_company)\
                .join(Profile, User.id_profile == Profile.id)\
                .filter(User.id == user_id)\
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
                        "date": user.date,
                    }
                    for user, company, headquarter, profile in db_users
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Users by headquarter (by user): {e}")
            self.db.rollback()
            return False


    def verify_used_user_info(self, email: str, username: str = None):
        try:
            db_user = self.db.query(User).filter(or_(User.username == username, User.email == email)).first()

            if db_user:
                if db_user.username == username:
                    return {"message": "El nombre de usuario ya está en uso", "id": db_user.id}
                elif db_user.email == email:
                    return {"message": "El correo ya está en uso", "id": db_user.id}

            return {"message": "Nombre y correo disponibles", "id": 0}

        except SQLAlchemyError as e:
            print(f"Error al obtener el usuario: {e}")
            self.db.rollback()
            return False


    def verify_user_state(self, id: int):
        try:
            db_user = self.db.query(User).filter(User.id == id).first()

            if db_user:
                if db_user.active:
                    return "Usuario activo"
                else:
                    return "Usuario inactivo"

            return False

        except SQLAlchemyError as e:
            print(f"Error verificando el estado del usuario: {e}")
            self.db.rollback()
            return False


    def register_user_db(self, user: UserCreate):
        try:
            db_user = User()
            
            db_user.name = user.name
            db_user.username = user.username
            db_user.email = user.email
            db_user.active = user.active            
            db_user.password = AuthService(db=self.db).hash_password(self.settings.TEMP_PASS)
            db_user.id_headquarter = 1
            db_user.id_profile = user.id_profile 
            db_user.is_first_login = True
            db_user.date = datetime.now()
            
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            
            return self.get_user_by_id(db_user.id)

        except SQLAlchemyError as e:
            print(f"Error registrando el usuario: {e}")
            self.db.rollback()
            return False


    def update_user_db(self, id: int, user: UserUpdate):
        try:
            db_user = self.db.query(User).filter(User.id == id).first()
            
            db_user.name = user.name
            db_user.username = user.username
            db_user.email = user.email
            db_user.active = user.active             
            db_user.id_headquarter = 1
            db_user.id_profile = user.id_profile  
            
            self.db.commit()
            
            return self.get_user_by_id(db_user.id)

        except SQLAlchemyError as e:
            print(f"Error actualizando el usuario: {e}")
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


    def get_logged_user_db(self, id: int):
        try:
            db_user = self.db.query(User, Headquarter, Company, Profile)\
                .join(Headquarter, User.id_headquarter == Headquarter.id)\
                .join(Company, Headquarter.id_company == Company.id)\
                .join(Profile, User.id_profile == Profile.id)\
                .filter(User.id == id)\
                .first()  

            if db_user:
                user, headquarter, company, profile = db_user
                db_permissions = self.get_logged_permissions_db(user.id)

                return {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "profile_name": profile.name,
                    "headquarter_name": headquarter.name,
                    "company_name": company.name,
                    "permissions": db_permissions,
                }

        except SQLAlchemyError as e:
            print(f"Error obteniendo la información del usuario logueado: {e}")
            self.db.rollback()
            return False
        
        
    def get_user_by_id(self, id: int):
        try:
            db_user = self.db.query(User, Headquarter, Company, Profile)\
                .join(Headquarter, User.id_headquarter == Headquarter.id)\
                .join(Company, Headquarter.id_company == Company.id)\
                .join(Profile, User.id_profile == Profile.id)\
                .filter(User.id == id)\
                .first()  

            if db_user:
                user, headquarter, company, profile = db_user

                return {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                    "profile_id": profile.id,
                    "profile_name": profile.name,
                    "headquarter_name": headquarter.name,
                    "company_name": company.name,
                    "active": user.active,
                }

        except SQLAlchemyError as e:
            print(f"Error obteniendo la información del usuario logueado: {e}")
            self.db.rollback()
            return False
