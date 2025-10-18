# Pet Embedding API

## Backend con FastAPI para generar embeddings de imágenes de mascotas, compararlas y autenticar cargas con ImageKit. Usa MobileNetV2 para extracción de características.

# Funcionalidades

- Generar embeddings de una sola imagen o en lote (batch).

- Comparar una imagen de mascota con la base de datos de mascotas perdidas usando similitud coseno.

- Autenticación segura para cargas a ImageKit.

- Preprocesamiento y normalización de imágenes con MobileNetV2.
# Tecnologías

- Python 3.10+
- FastAPI
- TensorFlow / Keras
- Pillow (PIL)
- NumPy / SciPy
- ImageKit
- Firebase-Admin

# Instalación
1. Clonar el repositorio
2. cd geopet-services
3. python -m venv venv
4. source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
5. pip install -r requirements.txt


Agrega tus claves de ImageKit en .env:
PUBLIC_API_KEY = "tu_public_api_key"
PRIVATE_API_KEY = "tu_private_api_key"

Agregar las credenciales de firebase en 
/credenciales/firebase-key.json

Inicia el servidor:

uvicorn main:app --reload

Documentación interactiva de la API:
http://127.0.0.1:8000/docs

# Endpoints
Embeddings (/embedding)

- POST /generate – Generar embedding de una imagen.
- POST /generate_batch – Generar embeddings de varias imágenes.
- POST /compare – Comparar imagen con mascotas perdidas.
- POST /detect_species – (No implementado aún)

ImageKit (/imagekit-auth)

- GET /imagekit-auth – Obtener token de autenticación para cargas seguras.


# Licencia

EK'BALAM LICENSE