import datetime
import os
from pathlib import Path

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
            db_company = Company()
            
            fields = ['name', 'nit', 'description', 'address', 'date']

            for field in fields:
                if company.get(field):
                    setattr(db_company, field, company[field])
            
            if company.get('img'):
                db_company.img = company['img']
                
            db_company.active = True
            db_company.date = datetime.now()
            
            self.db.add(db_company)
            self.db.commit()
            self.db.refresh(db_company)
            
            return db_company

        except SQLAlchemyError as e:
            print(f"Error adding Companys: {e}")
            self.db.rollback()
            return False
 

    def update_company_db(self, id: int, company: Company):
        try:
            exist_company = self.db.query(Company).filter(Company.id == id).first()
            
            if exist_company:
                exist_company.name = company['name']
                exist_company.nit = company['nit']
                exist_company.description = company['description']
                exist_company.address = company['address']
                exist_company.date = company['date']
                
                if company.get('img'):
                    exist_company.img = company['img']
                
                self.db.commit()
                
                return {
                    "id": exist_company.id,
                    "name": exist_company.name,
                    "nit": exist_company.nit,
                    "description": exist_company.description,
                    "address": exist_company.address,
                    "date": exist_company.date,
                    "active": exist_company.active,
                    "img": exist_company.img,
                }

        except SQLAlchemyError as e:
            print(f"Error deleting Companys: {e}")
            return False


    def delete_company_db(self, id: int):
        try:
            exist_company = self.db.query(Company).filter(Company.id == id).first()
            
            if exist_company:
                exist_company.active = False
                self.db.commit()
                
                return True
            else:
                return False

        except SQLAlchemyError as e:
            print(f"Error deleting Companys: {e}")
            return False
        
        
    def delete_old_image(self, image_path: str) -> bool:
        if not image_path:
            return False
        
        path = Path(image_path)
        if path.exists() and path.is_file():
            try:
                os.remove(path)
                return True
            except Exception as e:
                print(f"Error eliminando {path}: {e}")
                return False
        return False