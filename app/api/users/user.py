from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.user.user_service import UserService

router = APIRouter()

USERNAME = "Username"
USER_ID = "ID User"

@router.get("/users")
async def users(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    user_id: int = Query(None, title=USER_ID, description="The ID of the user which consult the users"),

):
    """Función utilizada para consultar la lista de usuarios.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información de los usuarios.
    """
    
    results = UserService(db).consult_users_db(user_id)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No users found.")

    return results

@router.get("/logged_user")
async def logged_user(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    username: str = Query(None, title=USERNAME, description="The username of the user to consult"),
):
    """Función utilizada para consultar la información del usuario logueado.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información del usuario logueado.
    """
    
    results = UserService(db).get_logged_user_db(username)

    return results

