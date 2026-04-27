from fastapi import APIRouter, Depends

from app.utils.global_functions import global_functions
from app.utils.config import get_settings
from app.utils.conn import db_manager

from app.services.smtp.smtp_service import SMTPService 

from app.schemas.schemas import EmailData

settings = get_settings()

router = APIRouter()

@router.post("/send-mail")
async def type_home(
    db: db_manager.session_local = Depends(db_manager.get_db), # type: ignore
    data: EmailData = None
):
    """Función utilizada para enviar un correo electrónico.

    Args:
        db (SessionLocal): Conexión de la base de datos. Defaults to Depends(get_db).
        data: Información a enviar en el correo

    Returns:
        obj: Retorna un objeto con la respuesta del envío.
    """

    result = await SMTPService(db).send_mail(data)

    if not result or (result.get('status') is not None and result.get('status') != 200):
        global_functions.get_exception_details("500", custom_detail="The email was not sent.")

    return result
