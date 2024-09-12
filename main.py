from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth.auth import router as routerAuth 
from app.api.company.company import router as routerCompany 
from app.api.products.product import router as routerProduct
from app.api.types.type import router as routerTypes 

from app.models.models import Base
from app.utils.conn import db_manager
from app.utils.init_db import DBInitializer

from app.utils.config import get_settings

settings = get_settings()

app = FastAPI()

origins = [
    settings.FRONTEND
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"], 
    allow_headers = ["*"], 
)

app.include_router(routerAuth,  tags=["Auth"])
app.include_router(routerCompany,  tags=["Company"])
app.include_router(routerProduct,  tags=["Products"])
app.include_router(routerTypes,  tags=["Types"])

db_initializer = DBInitializer(db_manager.session_local())

async def startup_event():
    Base.metadata.create_all(bind=db_manager.engine)
    db_initializer.init_db()

app.add_event_handler("startup", startup_event)
