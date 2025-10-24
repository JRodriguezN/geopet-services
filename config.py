import os
from dotenv import load_dotenv
import json
import base64

# Cargar variables del .env en local
load_dotenv()

# ImageKit
PUBLIC_API_KEY = os.getenv("PUBLIC_API_KEY")
PRIVATE_API_KEY = os.getenv("PRIVATE_API_KEY")

firebase_key_64 = os.getenv("FIREBASE_KEY")
FIREBASE_KEY =  json.loads(base64.b64decode(firebase_key_64).decode("utf-8"))






