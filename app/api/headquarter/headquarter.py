import json
from datetime import datetime

from fastapi import APIRouter, Depends, Query

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.headquarter.headquarter_service import HeadquarterService
from app.schemas.schemas import HeadquarterCreate, HeadquarterUpdate

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
    data: HeadquarterCreate = None
):
    """Función utilizada para registrar una nueva sede.

    Args:
        db: Conexión de la base de datos
        data: Objeto headquarter con los datos a insertar

    Returns:
        dict: Retorna un diccionario con la información de la sede creada.
    """
                                        
    result = HeadquarterService(db).register_headquarter_db(data)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No se pudo crear la sede.")

    return result

@router.put("/headquarter/{id}")
async def set_headquarter(
    id: int,
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    data: HeadquarterCreate = None
):
    """Función utilizada para registrar una nueva sede.

    Args:
        db: Conexión de la base de datos
        data: Objeto headquarter con los datos a insertar

    Returns:
        dict: Retorna un diccionario con la información de la sede creada.
    """
                                        
    result = HeadquarterService(db).update_headquarter_db(id, data)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No se pudo crear la sede.")

    return result
