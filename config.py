import os
from dotenv import load_dotenv

# Cargar variables del .env en local
load_dotenv()

# ImageKit
PUBLIC_API_KEY = os.getenv("PUBLIC_API_KEY")
PRIVATE_API_KEY = os.getenv("PRIVATE_API_KEY")



