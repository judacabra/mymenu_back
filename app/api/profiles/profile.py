import json

from fastapi import APIRouter, Depends, Query, Form
from typing import List, Dict, Any

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.profile.profile_service import ProfileService
from app.schemas.schemas import ProfileCreate

router = APIRouter()

ID = "ID Profile"

@router.get("/profiles")
async def profiles(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
):
    """Función utilizada para consultar la lista de perfiles.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información de los perfiles.
    """
    
    results = ProfileService(db).consult_profiles_db()

    if not results:
        global_functions.get_exception_details("404", custom_detail="No products found.")

    return results

@router.get("/profile_by_id/")
async def profile_by_id(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: int = Query(None, title=ID, description="The ID of the perfil to consult"),
):
    """Función utilizada para consultar la lista de perfiles.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).
        id (int): ID del perfil

    Returns:
        dict: Retorna un diccionario con la información del perfil por ID.
    """
    
    result = ProfileService(db).get_profile_by_id(id)

    if not result:
        global_functions.get_exception_details("404", custom_detail="No se encontró el perfil.")

    return result

@router.post("/profile")
async def set_profile(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    data: ProfileCreate = None
):
    """Función utilizada para registrar un nuevo producto.

    Args:
        db: Conexión de la base de datos
        product: Objeto Product con los datos a insertar
        img: (Opcional)

    Returns:
        dict: Retorna un diccionario con la información del nuevo perfil.
    """

    result = ProfileService(db).register_profile_db(data)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No creó el perfil.")

    return result

@router.put("/profile/{id}")
async def update_profile(
    id: int,
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    data: ProfileCreate = None
):
    """
    Función utilizada para actualizar un perfil.
    """

    result = ProfileService(db).update_profile_db(id, data)
        
    if not result:
        global_functions.get_exception_details("500", custom_detail="No se actualizó el perfil.")
        
    return result
