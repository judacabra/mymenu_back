from fastapi import APIRouter, Depends, Query

from app.utils.global_functions import global_functions
from app.utils.config import get_settings
from app.utils.conn import db_manager 

from app.services.types.types_service import TypeService

settings = get_settings()

COMPANY_ID = "ID Company"

router = APIRouter()

@router.get("/type/home")
async def type_home(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
):
    """Función utilizada para consultar la lista de opciones de tipo Home.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información del tipo Home.
    """
    id = 1
    results = TypeService(db).consult_type_db(id)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No home type found.")

    return results


@router.get("/type/menu")
async def type_menu(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    company_id: int = Query(None, title=COMPANY_ID, description="The ID of the user to consult"),
):
    """Función utilizada para consultar la lista de opciones de tipo Menu.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información del tipo Menu.
    """
    id_view = 2
    notData = 'Recomendaciones'
    results = TypeService(db).consult_type_db(id_view, company_id, None, notData)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No menu type found.")

    return results

@router.get("/type/recommended")
async def type_menu(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    company_id: int = Query(None, title=COMPANY_ID, description="The ID of the user to consult"),
):
    """Función utilizada para consultar la lista de opciones de tipo Menu recomendado.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información del tipo Menu.
    """
    id = 2
    filterdata = 'Recomendaciones'
    results = TypeService(db).consult_type_db(id, company_id, filterdata=filterdata)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No menu type found.")

    return results