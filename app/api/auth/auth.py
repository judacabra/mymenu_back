from datetime import timedelta
from fastapi import APIRouter, Depends
from typing import List, Dict, Any

from fastapi.security import OAuth2PasswordRequestForm
from app.services.user.auth_service import AuthService
from app.utils.global_functions import global_functions
from app.utils.conn import db_manager 

router = APIRouter()

@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: db_manager.session_local = Depends(db_manager.get_db) # type: ignore
    ):
    """Función utilizada para el login del usuario y la creación del token

    Args:

        form_data (OAuth2PasswordRequestForm, optional): Fatos del usuario ingresados en el formulario. Defaults to Depends().

        db (SessionLocal, optional): Conexión con la base de datos. Defaults to Depends(get_db)#type:ignore.
    """

    user = AuthService(db).authenticate_user(username=form_data.username, password=form_data.password)

    if user["message"] != "User found":
        global_functions.get_exception_details("401", custom_detail="Invalid credentials")


@router.post("/logout", response_model = List[Dict[str, Any]])
async def logout():
    query = "SELECT id, name, description, type, recommended, img, price FROM product;"
    response = await db_manager(query)
    
    if response is None or len(response) == 0:
        response = []
    
    columns = ["id", "name", "description", "type", "recommended", "img", "price"]
    results = [dict(zip(columns, row)) for row in response]
    
    return results