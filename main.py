from fastapi import FastAPI
from routes.vision_router import vision_router
from routes.upload_image_imagekitio import imagekitio

app =  FastAPI()

#200 Todo salio bien
#400 Bad request / datos mal enviados
#401 no autenticado
#404 no encontrado
#500 error interno del servidor

app.include_router(vision_router)
app.include_router(imagekitio)