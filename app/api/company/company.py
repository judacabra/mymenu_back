from fastapi import APIRouter, Depends, Query
from typing import Optional

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
        global_functions.get_exception_details("404", custom_detail="No company found.")

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
        global_functions.get_exception_details("404", custom_detail="No company info found.")

    return results

