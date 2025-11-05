from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_SENDER, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT


email_sender = APIRouter()

class EmailSchema(BaseModel):
    email: str
    subject: str
    message: str

def structure_email(email_data: EmailSchema):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = email_data.email
        msg['Subject'] = email_data.subject

        msg.attach(MIMEText(email_data.message, "html"))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
            
        print("✅ Correo enviado correctamente")
        # Lógica para enviar el correo electrónico
        return {"status": "Email sent successfully"}
    except Exception as e:
        print("❌ Error al enviar el correo:", str(e))
        return {"status": "Error", "message": str(e)}
    

@email_sender.post("/send_email")
async def send_email(email_data: EmailSchema, background_tasks: BackgroundTasks):
    background_tasks.add_task(structure_email, email_data)
    return {"status": "Email is being sent in the background"}