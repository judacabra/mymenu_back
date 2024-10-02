from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any, Optional

from app.utils.conn import db_manager 
from app.utils.global_functions import global_functions

from app.services.products.products_service import ProductService

USER_ID = "ID User"
COMPANY_ID = "ID Company"

router = APIRouter()

@router.get("/products")
async def products(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    user_id: Optional[int] = Query(None, title=USER_ID, description="The ID of the user which be the consult"),
    company_id: Optional[int] = Query(None, title=COMPANY_ID, description="The ID of the company be the consult"),

):
    """Función utilizada para consultar una lista de productos.

    Args:

        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).

    Returns:

        dict: Retorna un diccionario con la información de los productos.
    """

    if user_id is not None:
        results = ProductService(db).consult_product_db(user_id)

    if company_id is not None:
        results = ProductService(db).consult_product_by_company(company_id)

    if not results:
        global_functions.get_exception_details("404", custom_detail="No products found.")

    return results

