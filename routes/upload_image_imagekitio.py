from fastapi import APIRouter
import hashlib, hmac, time, secrets
import os
import base64

from config import PUBLIC_API_KEY, PRIVATE_API_KEY
from fastapi.responses import JSONResponse

imagekitio = APIRouter()


@imagekitio.get("/imagekit-auth")
def get_imagekit_auth():
    token =  secrets.token_hex(16)
    expire = int(time.time()) + 60 * 60 # 1hora
    
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