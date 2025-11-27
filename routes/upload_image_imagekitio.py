from fastapi import APIRouter, HTTPException
import hashlib, hmac, time, secrets
import os
import base64

from imagekitio import ImageKit
from pydantic import BaseModel

from config import PUBLIC_API_KEY, PRIVATE_API_KEY, IMAGEKIT_URL_ENDPOINT
from fastapi.responses import JSONResponse

imagekitio = APIRouter()

imagekit = ImageKit(
    public_key=PUBLIC_API_KEY,
    private_key=PRIVATE_API_KEY,
    url_endpoint=IMAGEKIT_URL_ENDPOINT,
)


@imagekitio.get("/imagekit-auth")
def get_imagekit_auth():
    token =  secrets.token_hex(16)
    expire = int(time.time()) + 1800 
    
    signature = hmac.new(
        PRIVATE_API_KEY.encode('utf-8'),
        f"{token}{expire}".encode('utf-8'),
        hashlib.sha1
    ).hexdigest()
    
    return JSONResponse({
        "token": token,
        "expire": expire,
        "signature":signature,
        "publicKey": PUBLIC_API_KEY
    })
class DeleteImageRequest(BaseModel):
    fileId: str

@imagekitio.post("/imagekit-delete")
def delete_image(req: DeleteImageRequest):
    try:
        print("Deleting image with fileId:", req.fileId)

        delete_response = imagekit.delete_file(req.fileId)
        print("DELETE_RESPONSE TYPE:", type(delete_response))
        print("DELETE_RESPONSE:", delete_response)
        #if delete_response.get("error"):
        #    raise HTTPException(status_code=500, detail=f"Error al eliminar la imagen: {delete_response['error']}")
        return {"message": "Imagen eliminada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")