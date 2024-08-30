from sqlalchemy import desc, or_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import os

from app.models.models import View


class ViewsService:

    def __init__(self, db: Session):
        self.db = db

    def consult_view_db(self, download_path: str = None, id: int = None, filter_data: str = None, name: str = None):
        try:
            file_path = rf"{download_path}/views" if download_path else ""
            query = self.db.query(View)

            if id is not None or name is not None:
                db_views = query.filter(or_(View.id == id, View.name == name)).first()
                if db_views:
                    return {
                        "id": db_views.id,
                        "name": db_views.name,
                        "description": db_views.description,
                        "icon": os.path.join(file_path, db_views.icon) if db_views.icon else None
                    }
                return {"id": 0}

            if filter_data is not None:
                filter_pattern = f"%{filter_data}%"
                query = query.filter(
                    or_(
                        View.name.ilike(filter_pattern),
                        View.description.ilike(filter_pattern)
                    )
                )

            db_views = query.order_by(desc(View.id)).all()

            if db_views:
                return [
                    {
                        "id": views.id,
                        "name": views.name,  # Corrección aquí
                        "description": views.description,  # Corrección aquí
                        "icon": os.path.join(file_path, views.icon) if views.icon else None
                    }
                    for views in db_views
                ]

            return False

        except SQLAlchemyError as e:
            print(f"Error getting views: {e}")
            self.db.rollback()
            return False


    def register_view_db(self, view):
        try:
            self.db.add(view)
            self.db.commit()
            self.db.refresh(view)
            return view
        except SQLAlchemyError as e:
            print(f"Error adding view: {e}")
            self.db.rollback()
            return False


    def modify_view_db(self, view):
        try:
            db_view = self.db.query(View).get(view.id)

            if not db_view:
                return False

            for key in [
                'name', 'description', 'icon'
            ]:
                if getattr(view, key) is not None:
                    setattr(db_view, key, getattr(view, key))

            self.db.commit()
            self.db.refresh(db_view)
            return db_view

        except SQLAlchemyError as e:
            print(f"Error modifying view: {e}")
            return False


    def delete_view_db(self, id: int):
        try:
            dependencies = self.get_view_dependencies(id)

            if not dependencies:
                db_view = self.db.query(View).filter(View.id == id).first()
                if db_view is not None:

                    self.db.delete(db_view)
                    self.db.commit()
                    return {"message": "view deleted"}
                else:
                    return {"error": "404", "message": "view not found"}

            return {"error": "400", "message": "view has dependencies"}

        except SQLAlchemyError as e:
            print(f"Error deleting view: {e}")
            return False
