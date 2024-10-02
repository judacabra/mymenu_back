from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import Type


class TypeService:

    def __init__(self, db: Session):
        self.db = db
        

    def consult_type_db(self, id_view: int, id_company: int = None, filterdata: str = None, notData: str = None):
        try:
            query = self.db.query(Type)

            if id_company is not None:
                query = query.filter(Type.id_company == id_company)

            if id_view is not None:
                query = query.filter(Type.id_view == id_view)

            if filterdata is not None:
                filterdata = f"%{filterdata}%"
                query = query.filter(Type.name.like(filterdata))

            if notData is not None:
                notData = f"%{notData}%"
                query = query.filter(~Type.name.like(notData))

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


    # def modify_types_db(self, types: dict):
        try:
            db_types = self.db.query(Type).get(types.id)

            if not db_types:
                return False

            for key in [
                'name', 'description', 'icon'
            ]:
                if getattr(types, key) is not None:
                    setattr(db_types, key, getattr(types, key))

            self.db.commit()
            self.db.refresh(db_types)
            return db_types

        except SQLAlchemyError as e:
            print(f"Error modifying types: {e}")
            return False


    # def delete_types_db(self, id: int):
        try:
            dependencies = self.get_types_dependencies(id)

            if not dependencies:
                db_types = self.db.query(Type).filter(Type.id == id).first()
                if db_types is not None:

                    self.db.delete(db_types)
                    self.db.commit()
                    return {"message": "types deleted"}
                else:
                    return {"error": "404", "message": "types not found"}

            return {"error": "400", "message": "types has dependencies"}

        except SQLAlchemyError as e:
            print(f"Error deleting types: {e}")
            return False
