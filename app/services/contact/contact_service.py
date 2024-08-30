from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import Contact

class ContactService:
    def __init__(self, db: Session):
        self.db = db

    def register_contact_db(self, contact: dict):
        try:
            self.db.add(contact)
            self.db.commit()
            self.db.refresh(contact)
            return contact

        except SQLAlchemyError as e:
            print(f"Error adding contact: {e}")
            self.db.rollback()
            return False


    def modify_contact_db(self, contact: dict):
        try:
            db_contact = self.db.query(Contact).get(contact.id)

            if not db_contact:
                return False

            for key in [
                'name', 'description'
            ]:
                if getattr(contact, key) is not None:
                    setattr(db_contact, key, getattr(contact, key))

            self.db.commit()
            self.db.refresh(db_contact)
            return db_contact

        except SQLAlchemyError as e:
            print(f"Error modifying contact: {e}")
            self.db.rollback()
            return False
