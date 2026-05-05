import json
from datetime import datetime
import os
import aiofiles

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from typing import Optional
from pathlib import Path

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.company.company_service import CompanyService

ID = "ID Company"
NAME = "Name Company"

router = APIRouter()

@router.get("/companies")
async def companies(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore

):
    """Función utilizada para consultar información de las empresas.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Retorna un diccionario con la información de las empresas.
    """
    
    results = CompanyService(db).consult_companies()

    if not results:
        global_functions.get_exception_details("404", custom_detail="No companies found.")

    return results

@router.get("/company_by_param")
async def company_by_param(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: Optional[int] = Query(None, title=ID, description="The ID of the company to consult"),
    name: Optional[str] = Query(None, title=NAME, description="The Name of the company to consult"),
):
    """Función utilizada para consultar la informacion de una empresa por id o nombre.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Retorna un diccionario con la información de una empresa.
    """
    if id:
        args = id, None

    if name:
        args = None, name

    results = CompanyService(db).get_company_by_param(*args)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No se encontró la empresa.")

    return results

@router.get("/companies_info")
async def companies_info(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore

):
    """Función utilizada para consultar información de empresas [total y activas].

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información de empresas [total y activas].
    """
    
    results = CompanyService(db).get_companies_info()

    if not results:
        global_functions.get_exception_details("404", custom_detail="No se encontró información de la empresa.")

    return results

@router.post("/company")
async def set_company(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    company_data: str = Form(...),
    img: Optional[UploadFile] = File(None),
):
    """Función utilizada para registrar una nueva empresa con posibilidad de subir imagen.

    Args:
        db: Conexión de la base de datos
        company_data: Objeto company con los datos a insertar
        img: Imagen de la empresa (opcional)

    Returns:
        dict: Retorna un diccionario con la información de la empresa creada.
    """
        
    upload_dir = Path("./uploads/company")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    db_company = json.loads(company_data)
            
    if img and img.filename:
        unique_suffix = f"{datetime.now().timestamp()}-{os.urandom(8).hex()}"
        file_extension = Path(img.filename).suffix
        filename = f"img-{unique_suffix}{file_extension}"
        file_path = upload_dir / filename
        
        try:
            content = await img.read()
            async with aiofiles.open(file_path, 'wb') as buffer:
                await buffer.write(content)
            
            db_company['img'] = str(file_path)
            
        except Exception as e:
            global_functions.get_exception_details("500", custom_detail="Error guardando la imagen de la empresa: " + f"{str(e)}")

    result = CompanyService(db).register_company_db(db_company)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No created company.")

    return result

@router.put("/company/{id}")
async def update_company(
    id: int,
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    company_data: str = Form(...),
    img: Optional[UploadFile] = File(None),
):
    """
    Función utilizada para actualizar una empresa con posibilidad de subir imagen.
    """
    
    upload_dir = Path("./uploads/company")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    db_company = json.loads(company_data)
            
    current_company = CompanyService(db).get_company_by_param(id, None)
    
    if img and img.filename:
        if current_company:
            CompanyService(db).delete_old_image(current_company.get('img'))
        
        unique_suffix = f"{datetime.now().timestamp()}-{os.urandom(8).hex()}"
        file_extension = Path(img.filename).suffix
        filename = f"img-{unique_suffix}{file_extension}"
        file_path = upload_dir / filename
        
        try:
            content = await img.read()
            async with aiofiles.open(file_path, 'wb') as buffer:
                await buffer.write(content)
            
            db_company['img'] = str(file_path)
            
        except Exception as e:
            global_functions.get_exception_details("500", custom_detail="Error saving image: " + f"{str(e)}")
    
    result = CompanyService(db).update_company_db(id, db_company)
        
    if not result:
        global_functions.get_exception_details("500", custom_detail="No updated company.")
        
    return result

@router.delete("/company_by_id")
async def delete_company(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: int = Query(None, title=ID, description="The ID of the company to delete"),
):
    """Función utilizada para eliminar una empresa.

    Args:
        db: Conexión de la base de datos
        id: ID de la empresa a eliminar

    Returns:
        dict: Retorna un estado del delete.
    """
        
    result = CompanyService(db).delete_company_db(id)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No deleted company.")

    return result