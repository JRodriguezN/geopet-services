from fastapi import FastAPI
from routes.vision_router import vision_router
from routes.upload_image_imagekitio import imagekitio
from routes.email_sender import email_sender
from routes.payment_route import payment_route

app =  FastAPI()

#200 Todo salio bien
#400 Bad request / datos mal enviados
#401 no autenticado
#404 no encontrado
#500 error interno del servidor

app.include_router(vision_router)
app.include_router(imagekitio)
app.include_router(email_sender)
app.include_router(payment_route)