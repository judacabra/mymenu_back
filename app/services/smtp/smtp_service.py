from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.schemas.schemas import EmailData

import smtplib
from email.message import EmailMessage

class SMTPService:

    def __init__(self, db: Session):
        self.db = db
        
    async def send_mail(self, data: EmailData):
        try:
            msg = EmailMessage()
            
            if data.body.strip().startswith('<!DOCTYPE') or data.body.strip().startswith('<html'):
                msg.set_content("Este correo requiere un cliente que soporte HTML")
                msg.add_alternative(data.body, subtype='html')
            else:
                msg.set_content(data.body)
            
            msg['Subject'] = data.subject
            msg['From'] = 'admin@mymenu.com.co'
            msg['To'] = data.to
            
            with smtplib.SMTP('localhost', 1025) as server:
                server.send_message(msg)
            
            return {
                "status": 200, 
                "message": "Correo enviado a MailHog"
            }
        except SQLAlchemyError as e:
            print(f"Error sending mail: {e}")
            return False