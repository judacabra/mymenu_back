from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import Headquarter, Type


class TypeService:

    def __init__(self, db: Session):
        self.db = db
        

    def consult_type_db(self, id_view: int, id_headquarter: int = None, filterdata: str = None, notData: str = None):
        try:
            query = self.db.query(Type)

            if id_view is not None:
                query = query.filter(Type.id_view == id_view)
                
            if id_view is not None and id_headquarter is not None:
                exist_headquarter = self.db.query(Headquarter).filter(Headquarter.id == id_headquarter).first()
                
                if exist_headquarter is not None:
                    query = query.filter(Type.id_headquarter == id_headquarter)
                else:
                    return False

            if filterdata is not None:
                filterdata = f"%{filterdata}%"
                query = query.filter(Type.name.like(filterdata))

            if notData is not None:
                notData = f"%{notData}%"
                query = query.filter(~Type.name.like(notData))

            print(str(query))
            db_types = query.all()

            if db_types:
                return [
                    {
                        "id": types.id,
                        "id_view": types.id_view, 
                        "name": types.name,  
                        "url": types.url,  
                    }
                    
                    for types in db_types
                ]

        except SQLAlchemyError as e:
            print(f"Error getting types: {e}")
            self.db.rollback()
            return False

        try:
            query = self.db.query(Type)

            db_types = query.filter(Type.id_view == 2).all()

            if db_types:
                return [
                    {
                        "id": types.id,
                        "id_view": types.id_view, 
                        "name": types.name,  
                        "url": types.url,  
                    }
                    for types in db_types
                ]

        except SQLAlchemyError as e:
            print(f"Error getting types: {e}")
            self.db.rollback()
            return False

    def register_type_db(self, type):
        try:
            self.db.add(type)
            self.db.commit()
            self.db.refresh(type)
            return type

        except SQLAlchemyError as e:
            print(f"Error adding types: {e}")
            self.db.rollback()
            return False
        
        
