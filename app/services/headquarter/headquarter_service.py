from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.schemas import HeadquarterCreate, HeadquarterUpdate
from app.models.models import Headquarter

class HeadquarterService:
    def __init__(self, db: Session):
        self.db = db

    def consult_headquarters(self):
        try:
            db_headquarters = self.db.query(Headquarter).all()

            if db_headquarters:
                return [
                    {
                        "id": headquarter.id,
                        "name": headquarter.name,
                        "description": headquarter.description,
                        "address": headquarter.address,
                        "active": headquarter.active,
                        "date": headquarter.date,
                    }
                    for headquarter in db_headquarters
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Companies: {e}")
            self.db.rollback()
            return False


    def get_total_headquarters(self):
        try:
            total_headquarters = self.db.query(func.count(Headquarter.id)).scalar()
            
            if total_headquarters is not None:
                return total_headquarters
            else:
                return 0

        except SQLAlchemyError as e:
            print(f"Error getting total headquarters: {e}")
            self.db.rollback()
            return False
   
   
    def get_headquarter_by_id(self, id: int):
        try:
            headquarter = self.db.query(Headquarter).filter(Headquarter.id == id).first()
            
            if headquarter:
                return {
                    "id": headquarter.id,
                    "name": headquarter.name,
                    "description": headquarter.description,
                    "address": headquarter.address,
                    "active": headquarter.active,
                }

        except SQLAlchemyError as e:
            print(f"Error obteniendola información de la sede: {e}")
            self.db.rollback()
            return False     


    def register_headquarter_db(self, headquarter: HeadquarterCreate):
        try:
            db_headquarter = Headquarter()
            
            db_headquarter.name = headquarter.name
            db_headquarter.description = headquarter.description
            db_headquarter.address = headquarter.address
            db_headquarter.active = headquarter.active
            db_headquarter.id_company = 1
            db_headquarter.date = datetime.now()
                                        
            self.db.add(db_headquarter)
            self.db.commit()
            self.db.refresh(db_headquarter)
            
            return db_headquarter

        except SQLAlchemyError as e:
            print(f"Error registrando la sede: {e}")
            self.db.rollback()
            return False
 

    def update_headquarter_db(self, id: int, headquarter: HeadquarterUpdate):
        try:
            exist_headquarter = self.db.query(Headquarter).filter(Headquarter.id == id).first()
            
            if exist_headquarter:
                exist_headquarter.name = headquarter.name
                exist_headquarter.description = headquarter.description
                exist_headquarter.address = headquarter.address
                exist_headquarter.active = headquarter.active
                                
                self.db.commit()
                
                return {
                    "id": exist_headquarter.id,
                    "name": exist_headquarter.name,
                    "description": exist_headquarter.description,
                    "address": exist_headquarter.address,
                    "active": exist_headquarter.active,
                    "date": exist_headquarter.date,
                }

        except SQLAlchemyError as e:
            print(f"Error actualizando la sede: {e}")
            self.db.rollback()
            return False
        

        try:
            exist_headquarter = self.db.query(Headquarter).filter(Headquarter.id == id).first()
            
            if exist_headquarter:
                exist_headquarter.active = False
                self.db.commit()
                
                return True
            else:
                return False

        except SQLAlchemyError as e:
            print(f"Error deleting Headquarters: {e}")
            return False