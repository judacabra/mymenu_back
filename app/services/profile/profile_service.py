from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import ProfilePermission, User, Profile, Permission

class ProfileService:
    def __init__(self, db: Session):
        self.db = db
        

    def get_profile_dependencies(self, id: int):
        try:
            query = self.db.query(User).filter(User.id_profile == id).first()

            if query is not None:
                return True
            else:
                return False

        except SQLAlchemyError as e:
            print(f"Error getting profile dependencies: {e}")
            return False


    def consult_permission_db(self):
        try:
            permission = self.db.query(Permission).all()

            if not permission:
                return False
            else:
                return permission

        except SQLAlchemyError as e:
            print(f"Error getting permissions: {e}")
            self.db.rollback()
            return False


    # def consult_profile_db(self, id: int = None, filter_data: str = None, name: str = None):
        try:
            query = self.db.query(Profile)

            if id is not None or name is not None:
                db_profile = query.filter(or_(Profile.id == id, Profile.name == name)).first()
                if db_profile:
                    permissions = self.db.query(ProfilePermission)\
                    .join(Permission, ProfilePermission.id_permission == Permission.id)\
                    .filter(ProfilePermission.id_profile == db_profile.id)\
                    .all()

                    permission_list = [
                        {
                            "id": perm.id,
                            "permission": {
                                "id": perm.permission.id,
                                "name": perm.permission.name
                            }
                        }
                        for perm in permissions
                    ]

                    return {
                        "id": db_profile.id,
                        "name": db_profile.name,
                        "description": db_profile.description,
                        "permissions": permission_list if permission_list else None
                    }
                return {"id": 0}

            if filter_data:
                filter_pattern = f"%{filter_data}%"
                query = query.filter(
                    or_(
                        Profile.name.ilike(filter_pattern),
                        Profile.description.ilike(filter_pattern)
                    )
                )

            db_profiles = query.order_by(desc(Profile.id)).all()

            if db_profiles:
                return [
                    {
                        "id": profile.id,
                        "name": profile.name,
                        "description": profile.description
                    }
                    for profile in db_profiles
                ]

            return False

        except SQLAlchemyError as e:
            print(f"Error getting profile: {e}")
            self.db.rollback()
            return False


    def consult_profiles_db(self):
        try:
            db_profiles = self.db.query(Profile)
        
            if db_profiles:
                return [
                    {
                        "id": profile.id,
                        "name": profile.name,
                        "description": profile.description,
                    }
                    for profile in db_profiles
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Products: {e}")
            self.db.rollback()
            return False


    # def consult_profile_db(self, id: int = None, filter_data: str = None, name: str = None):
    #     try:
    #         query = self.db.query(Profile)

    #         if id is not None or name is not None:
    #             db_profile = query.filter(or_(Profile.id == id, Profile.name == name)).first()
    #             if db_profile:
    #                 permissions = self.db.query(ProfilePermission)\
    #                 .join(Permission, ProfilePermission.id_permission == Permission.id)\
    #                 .filter(ProfilePermission.id_profile == db_profile.id)\
    #                 .all()

    #                 permission_list = [
    #                     {
    #                         "id": perm.id,
    #                         "permission": {
    #                             "id": perm.permission.id,
    #                             "name": perm.permission.name
    #                         }
    #                     }
    #                     for perm in permissions
    #                 ]

    #                 return {
    #                     "id": db_profile.id,
    #                     "name": db_profile.name,
    #                     "description": db_profile.description,
    #                     "permissions": permission_list if permission_list else None
    #                 }
    #             return {"id": 0}

    #         if filter_data:
    #             filter_pattern = f"%{filter_data}%"
    #             query = query.filter(
    #                 or_(
    #                     Profile.name.ilike(filter_pattern),
    #                     Profile.description.ilike(filter_pattern)
    #                 )
    #             )

    #         db_profiles = query.order_by(desc(Profile.id)).all()

    #         if db_profiles:
    #             return [
    #                 {
    #                     "id": profile.id,
    #                     "name": profile.name,
    #                     "description": profile.description
    #                 }
    #                 for profile in db_profiles
    #             ]

    #         return False

    #     except SQLAlchemyError as e:
    #         print(f"Error getting profile: {e}")
    #         self.db.rollback()
    #         return False


    def register_profile_db(self, profile):
        try:
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)
            return profile

        except SQLAlchemyError as e:
            print(f"Error adding profile: {e}")
            self.db.rollback()
            return False


    def modify_profile_db(self, profile):
        try:
            db_profile = self.db.query(Profile).get(profile.id)

            if not db_profile:
                return False

            for key in [
                'name', 'description'
            ]:
                if getattr(profile, key) is not None:
                    setattr(db_profile, key, getattr(profile, key))

            self.db.commit()
            self.db.refresh(db_profile)
            return db_profile

        except SQLAlchemyError as e:
            print(f"Error modifying user: {e}")
            self.db.rollback()
            return False


    def register_profile_permission_db(self, profile_permission):
        try:
            self.db.add(profile_permission)
            self.db.commit()
            self.db.refresh(profile_permission)
            return profile_permission
        except SQLAlchemyError as e:
            print(f"Error adding profile permission: {e}")
            self.db.rollback()
            return False


    def delete_profile_permission_db(self, profile_permission):
        try:
            self.db.delete(profile_permission)
            self.db.commit()
            return {"message": "Profile Permission deleted"}

        except SQLAlchemyError as e:
            print(f"Error deleting permission: {e}")
            return False


    def delete_profile_db(self, id: int):
        try:
            dependencies = self.get_profile_dependencies(id)

            if not dependencies:
                db_profile = self.db.query(Profile).filter(Profile.id == id).first()
                if db_profile is not None:

                    self.db.delete(db_profile)
                    self.db.commit()
                    return {"message": "Profile deleted"}
                else:
                    return {"error": "404", "message": "Profile not found"}

            return {"error": "400", "message": "Profile has dependencies"}

        except SQLAlchemyError as e:
            print(f"Error deleting profile: {e}")
            return False
