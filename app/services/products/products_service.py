from sqlalchemy import desc, or_, and_
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import json
from app.models.models import Company, Product, Profile, User

class ProductService:
    def __init__(self, db: Session):
        self.db = db

    def consult_product_db(self, user_id: int):
        try:
            db_user = self.db.query(User, Profile)\
                .join(Profile, User.id_profile == Profile.id)\
                .filter(User.id == user_id)\
                .filter(Product.status == True)\
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
                        "stock": product.stock,
                        "status": product.status,
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

            query = query.filter(Product.status == True)
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
                        "stock": product.stock,
                        "status": product.status
                    }
                    for product, company in db_products
                ]

        except SQLAlchemyError as e:
            print(f"Error getting Products by company: {e}")
            self.db.rollback()
            return False


    def register_product_db(self, product: dict):
        try:
            db_product = Product()
            
            fields = ['name', 'description', 'id_type', 'recommended', 'price', 'stock', 'id_company']

            for field in fields:
                if product.get(field):
                    setattr(db_product, field, product[field])
            
            if product.get('img'):
                db_product.img = product['img']
                
            db_product.status = True
            
            self.db.add(db_product)
            self.db.commit()
            self.db.refresh(db_product)
            
            return db_product

        except SQLAlchemyError as e:
            print(f"Error adding Products: {e}")
            self.db.rollback()
            return False
        
        
    def get_product_by_id(self, id: int):
        try:
            query = self.db.query(Product)

            if id is not None:
                query = query.filter(Product.id == id)

            product = query.first()

            if product:
                return {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "id_type": product.id_type,
                    "recommended": product.recommended,
                    "price": product.price,
                    "stock": product.stock,
                    "status": product.status,
                    "img": product.img,
                }

        except SQLAlchemyError as e:
            print(f"Error getting Product: {e}")
            self.db.rollback()
            return False


    def update_product_db(self, id: int, product: Product):
        try:
            exist_product = self.db.query(Product).filter(Product.id == id).first()
            
            if exist_product:
                exist_product.name = product['name']
                exist_product.description = product['description']
                exist_product.id_type = product['id_type']
                exist_product.recommended = product['recommended']
                exist_product.price = product['price']
                exist_product.stock = product['stock']
                
                if product.get('img'):
                    exist_product.img = product['img']
                
                self.db.commit()
                
                return {
                    "id": exist_product.id,
                    "name": exist_product.name,
                    "description": exist_product.description,
                    "id_type": exist_product.id_type,
                    "recommended": exist_product.recommended,
                    "price": exist_product.price,
                    "stock": exist_product.stock,
                    "status": exist_product.status,
                    "img": exist_product.img,
                }

        except SQLAlchemyError as e:
            print(f"Error deleting Products: {e}")
            return False


    def delete_product_db(self, id: int):
        try:
            exist_product = self.db.query(Product).filter(Product.id == id).first()
            
            if exist_product:
                exist_product.status = False
                self.db.commit()
                
                return True
            else:
                return False

        except SQLAlchemyError as e:
            print(f"Error deleting Products: {e}")
            return False