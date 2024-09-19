from fastapi import APIRouter, Depends
from typing import List, Dict, Any

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.profile.profile_service import ProfileService

router = APIRouter()

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

