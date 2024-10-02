from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.models import Company, Product, Profile, User

class ProductService:

    def __init__(self, db: Session):
        self.db = db
        

    def consult_product_db(self, user_id: int):
        try:
            db_user = self.db.query(User, Profile)\
                .join(Profile, User.id_profile == Profile.id)\
                .filter(User.id == user_id)\
                .first() 
            
            if db_user:
                user, profile = db_user
                
                if profile.id == 1:
                    db_products = self.consult_product_by_superadmin()
                else:
                    db_products = self.consult_product_by_company(user.id_company)

                return db_products
                

        except SQLAlchemyError as e:
            print(f"Error getting Products: {e}")
            self.db.rollback()
            return False


    def consult_product_by_superadmin(self):
        try:
            db_products = self.db.query(Product, Company)\
                .join(Company, Product.id_company == Company.id)\
                .all()     
            
            if db_products:
                return [
                    {
                        "id": product.id,
                        "company_name": company.name,
                        "name": product.name,
                        "description": product.description,
                        "id_type": product.id_type,
                        "recommended": product.recommended,
                        "img": product.img,
                        "price": product.price,
                        "pricsadfe": 'putamadre',
                        "stock": product.stock
                    }

                    for product, company in db_products
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Products by superadmin: {e}")
            self.db.rollback()
            return False


    def consult_product_by_company(self, id_company: int):
        try:
            query = self.db.query(Product, Company)\
                .join(Company, Product.id_company == Company.id)

            if id_company is not None:
                query =  query.filter(Company.id == id_company)

            db_products = query.all()

            if db_products:
                return [
                    {
                        "id": product.id,
                        "company_name": company.name,
                        "name": product.name,
                        "description": product.description,
                        "id_type": product.id_type,
                        "recommended": product.recommended,
                        "img": product.img,
                        "price": product.price,
                        "stock": product.stock
                    }
                    for product, company in db_products
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Products by company: {e}")
            self.db.rollback()
            return False


    def register_product_db(self, product):
        try:
            self.db.add(Product)
            self.db.commit()
            self.db.refresh(Product)
            return Product

        except SQLAlchemyError as e:
            print(f"Error adding Products: {e}")
            self.db.rollback()
            return False


    # def modify_Products_db(self, Products: dict):
        try:
            db_products = self.db.query(Product).get(Products.id)

            if not db_products:
                return False

            for key in [
                'name', 'description', 'icon'
            ]:
                if getattr(Products, key) is not None:
                    setattr(db_products, key, getattr(Products, key))

            self.db.commit()
            self.db.refresh(db_products)
            return db_products

        except SQLAlchemyError as e:
            print(f"Error modifying Products: {e}")
            return False


    # def delete_Products_db(self, id: int):
        try:
            dependencies = self.get_Products_dependencies(id)

            if not dependencies:
                db_products = self.db.query(Product).filter(Product.id == id).first()
                if db_products is not None:

                    self.db.delete(db_products)
                    self.db.commit()
                    return {"message": "Products deleted"}
                else:
                    return {"error": "404", "message": "Products not found"}

            return {"error": "400", "message": "Products has dependencies"}

        except SQLAlchemyError as e:
            print(f"Error deleting Products: {e}")
            return False
