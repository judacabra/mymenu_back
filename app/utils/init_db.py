from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import Company, Contact, View, Type, Permission, Profile, User 

from app.schemas.schemas import UserCreate, ProfileCreate, CompanyCreate, ContactCreate, ViewCreate, TypeCreate

from app.services.types.types_service import TypeService
from app.utils.config import get_settings
from app.utils.global_functions import GlobalFunctions

from app.services.user.auth_service import AuthService
from app.services.user.user_service import UserService
from app.services.views.views_service import ViewsService
from app.services.profile.profile_service import ProfileService
from app.services.company.company_service import CompanyService
from app.services.contact.contact_service import ContactService


class DBInitializer:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.settings = get_settings()


    def init_db(self):
        try:
            if not self.check_company():
                self.create_initial_company()
            if not self.check_contact():
                self.create_initial_contact()
            if not self.check_views():
                self.create_initial_views()
            if not self.check_types():
                self.create_initial_types()
            if not self.check_permissions():
                self.create_initial_permissions()
            if not self.check_profiles():
                self.create_initial_profiles()
            if not self.check_users():
                self.create_initial_user()
        except Exception as e:
            print(f"Error initializing database: {e}")
            raise


    def check_company(self) -> bool:
        company_count = self.db.query(Company).count()
        return company_count > 0
    
    def check_contact(self) -> bool:
        contact_count = self.db.query(Contact).count()
        return contact_count > 0
    
    def check_views(self) -> bool:
        view_count = self.db.query(View).count()
        return view_count > 0
    
    def check_types(self) -> bool:
        type_count = self.db.query(Type).count()
        return type_count > 0

    def check_permissions(self) -> bool:
        permissions_count = self.db.query(Permission).count()
        return permissions_count > 0

    def check_profiles(self) -> bool:
        profile_count = self.db.query(Profile).count()
        return profile_count > 0
    
    def check_users(self) -> bool:
        user_count = self.db.query(User).count()
        return user_count > 0

    def create_initial_company(self):
        try:
            initial_company = CompanyCreate(
                name = "DevSoftone",
                nit = "1144202047",
                description = "Empresa de desarrollo de software",
                address = "Centro Comercial Chipichape",
                active = True
            )

            company_db = Company(**initial_company.model_dump())
            CompanyService(db=self.db).register_company_db(company_db)

            return company_db
        except Exception as e:
            self.db.rollback()
            print(f"Error trying to add the company: {e}")
      
    def create_initial_contact(self):
        try:
            initial_contact = ContactCreate(
                id_company=1,
                number=3160553500,
                message="Jhon"
            )

            contact_db = Contact(**initial_contact.model_dump())
            ContactService(db=self.db).register_contact_db(contact_db)

            return contact_db
        except Exception as e:
            self.db.rollback()
            print(f"Error trying to add the contact: {e}")

    def create_initial_views(self):
        try:
            initial_views_data = [
                ViewCreate(name="Home"),
                ViewCreate(name="Menu"),
            ]

            added_views = []
            for view_data in initial_views_data:
                view_db = View(**view_data.model_dump())  
                result = ViewsService(db=self.db).register_view_db(view_db)
                if result:
                    added_views.append(result)

            return added_views
        except Exception as e:
            self.db.rollback()
            print(f"Error trying to add the initial views: {e}")

    def create_initial_types(self):
        try:
            initial_types = [
                TypeCreate(
                    id_view = 1,
                    name = 'Carta',
                    url = 'restaurant/menu',
                ),
                TypeCreate(
                    id_view = 1,
                    name = 'Reservas',
                    url = 'restaurant/bookings',
                ),
                TypeCreate(
                    id_view = 1,
                    name = 'Contacto',
                    url = 'https://api.whatsapp.com/send?phone=57${this.contacto.numero}&text=${this.contacto.mensaje}',
                ),
                TypeCreate(
                    id_view = 2,
                    name = 'Recomendaciones del chef',
                    url = 'recomendaciones',
                ),
                TypeCreate(
                    id_view = 2,
                    name = 'Entradas',
                    url = 'entradas',
                ),
                TypeCreate(
                    id_view = 2,
                    name = 'Fuertes',
                    url = 'fuertes',
                ),
                TypeCreate(
                    id_view = 2,
                    name = 'Bebidas',
                    url = 'bebidas',
                ),
            ]

            added_types = []
            for type_data in initial_types:
                type_db = Type(**type_data.model_dump())  
                result = TypeService(db=self.db).register_type_db(type_db)
                if result:
                    added_types.append(result)

            return added_types
        except Exception as e:
            self.db.rollback()
            print(f"Error trying to add the initial types: {e}")

    def create_initial_permissions(self):
        try:
            initial_permission = [
                Permission(
                    id=1,
                    name="Profile",
                    description="Profile Parameter"
                ),
                Permission(
                    id=2,
                    name="User",
                    description="User Parameter"
                ),
                Permission(
                    id=3,
                    name="Product",
                    description="Product Parameter"
                ),
                Permission(
                    id=4,
                    name="Company",
                    description="Company Parameter"
                ),
                Permission(
                    id=5,
                    name="Type",
                    description="Type Parameter"
                )
            ]

            added_permissions = []
            for permission in initial_permission:
                added_permission = self.add_permission_db(permission)
                if added_permission:
                    added_permissions.append(added_permission)

            return added_permissions
        except Exception as e:
            self.db.rollback()
            print(f"Error trying to add the initial permissions: {e}")

    def add_permission_db(self, permission: Permission):
        try:
            self.db.add(permission)
            self.db.commit()
            self.db.refresh(permission)
            return permission

        except SQLAlchemyError as e:
            print(f"Error adding permissions: {e}")
            self.db.rollback()
            return False

    def create_initial_profiles(self):
        try:
            initial_profile = ProfileCreate(
                name="Admin Profile",
                description="Admin Profile",
                id_permission=1
            )

            profile_db = Profile(**initial_profile.model_dump())
            ProfileService(db=self.db).register_profile_db(profile_db)

            return profile_db
        except Exception as e:
            self.db.rollback()
            print(f"Error trying to add the profile: {e}")

    def create_initial_user(self):
        try:
            hashed_password = AuthService(db=self.db).hash_password(self.settings.TEMP_PASS)

            profile = self.db.query(Profile.id).first()
            if profile is None:
                raise ValueError("No se encontró ningún perfil para asignar al usuario.")
            
            company = self.db.query(Company.id).first()
            if company is None:
                raise ValueError("No se encontró ningúna compañia para asignar al usuario.")

            profile_id = profile.id
            company_id = company.id

            initial_user = UserCreate(
                name=self.settings.NAME_USER,
                username=self.settings.USERNAME_USER,
                email=self.settings.EMAIL_USER,
                password=hashed_password,
                id_profile=profile_id,
                id_company=company_id,
                active=True
            )

            user_db = User(**initial_user.model_dump())
            UserService(db=self.db).register_user_db(user_db)
        except Exception as e:
            self.db.rollback()
            print(f"Error trying to add the initial user: {e}")
