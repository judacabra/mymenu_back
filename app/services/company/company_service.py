from sqlalchemy import desc, func, or_, and_, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import unicodedata

from app.models.models import Company

class CompanyService:
    def __init__(self, db: Session):
        self.db = db

    def normalizar_texto(self, texto: str):
        if texto is None:
            return ""
        texto = texto.replace(" ", "")
        texto = unicodedata.normalize('NFD', texto).encode('ascii', 'ignore').decode('utf-8')
        return texto.lower()

    def consult_companies(self):
        try:
            db_companies = self.db.query(Company).all()

            if db_companies:
                return [
                    {
                        "id": company.id,
                        "name": company.name,
                        "nit": company.nit,
                        "description": company.description,
                        "address": company.address,
                        "img": company.img,
                        "active": company.active,
                    }
                    for company in db_companies
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Companies: {e}")
            self.db.rollback()
            return False


    def get_company_by_param(self, id: int = None, name: str = None):
        try:
            query = self.db.query(Company)

            if id is not None:
                query = query.filter(Company.id == id)

            if name is not None:
                company_name = self.normalizar_texto(name)
                
                stmt = select(Company).where(
                    func.lower(func.replace(Company.name, ' ', '')) == company_name
                ).limit(1)
                   
                query = query.filter(company_name == name) 

            company = query.first()

            if company:
                return {
                    "id": company.id,
                    "name": company.name,
                    "nit": company.nit,
                    "description": company.description,
                    "address": company.address,
                    "img": company.img,
                    "active": company.active,
                }

        except SQLAlchemyError as e:
            print(f"Error getting Company: {e}")
            self.db.rollback()
            return False
        

    def get_total_companies(self):
        try:
            total_companies = self.db.query(func.count(Company.id)).scalar()
            
            if total_companies is not None:
                return total_companies
            else:
                return 0

        except SQLAlchemyError as e:
            print(f"Error getting total companies: {e}")
            self.db.rollback()
            return False
        

    def get_companies_active(self):
        try:
            companies_active = self.db.query(func.count()).filter(Company.active == True).scalar()
            
            if companies_active is not None:
                return companies_active
            else:
                return 0

        except SQLAlchemyError as e:
            print(f"Error getting companies active: {e}")
            self.db.rollback()
            return False


    def get_companies_info(self):
        try:
            total_companies = self.get_total_companies()
            companies_active = self.get_companies_active()
            company_info = {'total': 0, 'active': 0}

            if total_companies is not None and total_companies > 0:
                company_info['total'] = total_companies

            if companies_active is not None and companies_active > 0:
                company_info['active'] = companies_active

            return company_info
           
        except SQLAlchemyError as e:
            print(f"Error getting Company: {e}")
            self.db.rollback()
            return False


    def register_company_db(self, company: dict):
        try:
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)
            return company

        except SQLAlchemyError as e:
            print(f"Error adding company: {e}")
            self.db.rollback()
            return False


    def modify_company_db(self, company: dict):
        try:
            db_company = self.db.query(Company).get(company.id)

            if not db_company:
                return False

            for key in [
                'name', 'description'
            ]:
                if getattr(company, key) is not None:
                    setattr(db_company, key, getattr(company, key))

            self.db.commit()
            self.db.refresh(db_company)
            return db_company

        except SQLAlchemyError as e:
            print(f"Error modifying company: {e}")
            self.db.rollback()
            return False
