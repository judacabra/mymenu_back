from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import Company

class CompanyService:
    def __init__(self, db: Session):
        self.db = db

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
