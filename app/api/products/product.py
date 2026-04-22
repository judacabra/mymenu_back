from types import SimpleNamespace

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

import os
import shutil
import aiofiles
import json

from datetime import datetime
from pathlib import Path
from typing import Optional

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.products.products_service import ProductService
from app.schemas.schemas import ProductCreate, ProductUpdate
from app.models.models import Product

ID = "ID Product"
USER_ID = "ID User"
COMPANY_ID = "ID Company"

router = APIRouter()

@router.get("/products")
async def products(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    user_id: Optional[int] = Query(None, title=USER_ID, description="The ID of the user which be the consult"),
    company_id: Optional[int] = Query(None, title=COMPANY_ID, description="The ID of the company be the consult"),

):
    """Función utilizada para consultar una lista de productos.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Retorna un diccionario con la información de los productos.
    """

    if user_id is not None:
        results = ProductService(db).consult_product_db(user_id)

    if company_id is not None:
        results = ProductService(db).consult_product_by_company(company_id)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No products found.")

    return results

@router.get("/product_by_id")
async def product_by_id(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: int = Query(None, title=ID, description="The ID of the product to consult"),
):
    """Función utilizada para consultar la informacion de un producto por id.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).
        id INT: ID del producto a buscar

    Returns:
        dict: Retorna un diccionario con la información de una empresa.
    """
    
    results = ProductService(db).get_product_by_id(id)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No product found.")

    return results

@router.post("/products")
async def set_product(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    product_data: str = Form(...),
    img: Optional[UploadFile] = File(None),
):
    """Función utilizada para registrar un nuevo producto.

    Args:
        db: Conexión de la base de datos
        product: Objeto Product con los datos a insertar

    Returns:
        dict: Retorna un diccionario con la información del producto creado.
    """
        
    upload_dir = Path("./uploads/product")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    db_product = json.loads(product_data)
            
    if img and img.filename:
        unique_suffix = f"{datetime.now().timestamp()}-{os.urandom(8).hex()}"
        file_extension = Path(img.filename).suffix
        filename = f"img-{unique_suffix}{file_extension}"
        file_path = upload_dir / filename
        
        try:
            content = await img.read()
            async with aiofiles.open(file_path, 'wb') as buffer:
                await buffer.write(content)
            
            db_product['img'] = str(file_path)
            
        except Exception as e:
            global_functions.get_exception_details("500", custom_detail="Error saving image: " + f"{str(e)}")

    results = ProductService(db).register_product_db(db_product)

    if not results:
        global_functions.get_exception_details("500", custom_detail="No created product.")

    return results

@router.put("/product/{id}")
async def update_product(
    id: int,
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    product_data: str = Form(...),
    img: Optional[UploadFile] = File(None),
):
    """
    Función utilizada para actualizar un producto con posibilidad de subir imagen.
    """
    
    upload_dir = Path("./uploads/product")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    db_product = json.loads(product_data)
            
    if img and img.filename:
        unique_suffix = f"{datetime.now().timestamp()}-{os.urandom(8).hex()}"
        file_extension = Path(img.filename).suffix
        filename = f"img-{unique_suffix}{file_extension}"
        file_path = upload_dir / filename
        
        try:
            content = await img.read()
            async with aiofiles.open(file_path, 'wb') as buffer:
                await buffer.write(content)
            
            db_product['img'] = str(file_path)
            
        except Exception as e:
            global_functions.get_exception_details("500", custom_detail="Error saving image: " + f"{str(e)}")
    
    results = ProductService(db).update_product_db(id, db_product)
        
    if not results:
        global_functions.get_exception_details("500", custom_detail="No updated product.")
        
    return results

@router.delete("/product_by_id")
async def delete_product(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: int = Query(None, title=ID, description="The ID of the product to delete"),
):
    """Función utilizada para eliminar un producto.

    Args:
        db: Conexión de la base de datos
        id: ID del producto a eliminar

    Returns:
        dict: Retorna un estado del delete.
    """
        
    results = ProductService(db).delete_product_db(id)

    if not results:
        global_functions.get_exception_details("500", custom_detail="No deleted product.")

    return results