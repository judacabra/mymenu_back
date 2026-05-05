import json
from datetime import datetime
import os
import aiofiles

from fastapi import APIRouter, Depends, Query, UploadFile, File, Form
from typing import Optional
from pathlib import Path

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.headquarter.headquarter_service import HeadquarterService
from app.schemas.schemas import HeadquarterUpdate

ID = "ID Headquarter"
NAME = "Name Headquarter"

router = APIRouter()

@router.get("/headquarters")
async def get_headquarters(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore

):
    """Función utilizada para consultar información de las empresas.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Retorna un diccionario con la información de las empresas.
    """
    
    results = HeadquarterService(db).consult_headquarters()

    if not results:
        global_functions.get_exception_details("404", custom_detail="No headquarters found.")

    return results

@router.get("/headquarter_by_id")
async def get_headquarter_by_id(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: int = Query(None, title=ID, description="The ID of the headquarter to consult"),
):
    """Función utilizada para buscar una sede por id.

    Args:
        db: Conexión de la base de datos
        id: ID de la empresa a consultar

    Returns:
        dict: Retorna un diccionario con la data de la sede
    """
        
    result = HeadquarterService(db).get_headquarter_by_id(id)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No se encontró la sede.")

    return result

@router.post("/headquarter")
async def set_headquarter(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    headquarter_data: str = Form(...),
    img: Optional[UploadFile] = File(None),
):
    """Función utilizada para registrar una nueva empresa con posibilidad de subir imagen.

    Args:
        db: Conexión de la base de datos
        headquarter_data: Objeto headquarter con los datos a insertar
        img: Imagen de la empresa (opcional)

    Returns:
        dict: Retorna un diccionario con la información de la empresa creada.
    """
        
    upload_dir = Path("./uploads/headquarter")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    db_headquarter = json.loads(headquarter_data)
            
    result = HeadquarterService(db).register_headquarter_db(db_headquarter)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No created headquarter.")

    return result
