from fastapi import APIRouter
from typing import List, Dict, Any
from app.utils.conn import db_manager 

router = APIRouter()

@router.get("/products", response_model = List[Dict[str, Any]])
async def products():
    query = "SELECT id, name, description, type, recommended, img, price FROM product;"
    response = await db_manager(query)
    
    if response is None or len(response) == 0:
        response = []
    
    columns = ["id", "name", "description", "type", "recommended", "img", "price"]
    results = [dict(zip(columns, row)) for row in response]
    
    return results

