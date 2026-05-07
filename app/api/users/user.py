from datetime import timedelta
import json

from fastapi import APIRouter, Depends, Query, Form
from typing import Optional

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.user.user_service import UserService
from app.schemas.schemas import UserCreate, UserUpdate
from app.services.user.auth_service import AuthService
from app.utils.config import get_settings

router = APIRouter()

USERNAME = "Username"
USER_ID = "ID User"
settings = get_settings()

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

@router.get("/user_by_id")
async def user_by_id(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: int = Query(None, title=USER_ID, description="The ID of the user to consult"),
):
    """Función utilizada para consultar la informacion de un producto por id.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).
        id INT: ID del producto a buscar

    Returns:
        dict: Retorna un diccionario con la información de un usuario.
    """
    
    result = UserService(db).get_user_by_id(id)

    if not result:
        global_functions.get_exception_details("404", custom_detail="No se encontró el usuario.")

    return result

@router.get("/logged_user")
async def logged_user(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    id: int = Query(None, title=USERNAME, description="The username of the user to consult"),
):
    """Función utilizada para consultar la información del usuario logueado.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información del usuario logueado.
    """
    
    results = UserService(db).get_logged_user_db(id)

    return results

@router.post("/user")
async def set_user(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    data: UserCreate = None
):
    """Función utilizada para registrar un nuevo usuario.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Retorna un diccionario con la información del nuevo usuario.
    """
        
    result = UserService(db).register_user_db(data)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No se pudo crear el usuario.")

    return result

@router.put("/user/{id}")
async def update_product(
    id: int,
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    data: UserUpdate = None
):
    """Función utilizada para registrar un nuevo usuario.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:
        dict: Retorna un diccionario con la información del nuevo usuario.
    """
    
    result = UserService(db).update_user_db(id, data)

    if not result:
        global_functions.get_exception_details("500", custom_detail="No se pudo actualizar el usuario.")

    return result

@router.put("/user/change-password/{id}")
async def update_product(
    id: int,
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    data: dict = None
):
    """Función utilizada para cambiar la constraseña de un usuario.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).
        id: int = ID del usuario
        data: any = Nueva contraseña y confirmacion de contraseña

    Returns:
        dict: Retorna una bandera, del estado del cambio de contraseña
    """
    
    result = UserService(db).update_password_db(id, data)

    if not result["success"]:
        global_functions.get_exception_details("400", custom_detail=result["message"])

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService(db).create_access_token(
        data={"sub": str(result["user"]["id"])}, 
        expires_delta=access_token_expires, 
        secret_key=settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )

    result["access_token"] = access_token

    return result