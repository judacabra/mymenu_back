from fastapi import APIRouter
from typing import List, Dict, Any
from app.utils.conn import db_manager 

router = APIRouter()

@router.post("/login", response_model = List[Dict[str, Any]])
async def login():
    query = "SELECT authenticate_user($1, $2);"
    response = await db_manager(query)
    
    return response

@router.post("/logout", response_model = List[Dict[str, Any]])
async def logout():
    query = "SELECT id, name, description, type, recommended, img, price FROM product;"
    response = await db_manager(query)
    
    if response is None or len(response) == 0:
        response = []
    
    columns = ["id", "name", "description", "type", "recommended", "img", "price"]
    results = [dict(zip(columns, row)) for row in response]
    
    return results