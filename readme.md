# Pet Embedding API

Backend con FastAPI para generar embeddings de imágenes de mascotas, compararlas y autenticar cargas con ImageKit. Usa MobileNetV2 para extracción de características.

---

## 1. Estructura del repositorio

- `Dockerfile` – Imagen de la API con FastAPI + TensorFlow + Firebase.
- `docker-compose.monitoring.yml` – Stack de monitoreo (API + Prometheus + Node Exporter + Grafana).
- `.github/workflows/` – Pipelines de CI/CD:
    - `test.yml` – Ejecuta tests/lint básicos.
    - `deploy.yml` – Build & push de imagen Docker a GHCR.
- `scripts/` – Scripts auxiliares:
    - `run_tests.sh` – Ejecuta validación rápida del código.
    - `build_image.sh` – Construye la imagen Docker local.
    - `run_local.sh` – Levanta la API local con uvicorn.
    - `deploy_docker.sh` – Ejemplo para build/push de imagen.
    - `start_monitoring.sh` – Levanta stack de monitoreo con docker compose.
- `prometheus.yml` / `alerts.yml` – Configuración de Prometheus y alertas.

---

## 2. Tecnologías

- Python 3.11
- FastAPI
- TensorFlow / Keras (CPU)
- Pillow (PIL)
- NumPy / SciPy
- ImageKit
- Firebase-Admin
- Prometheus + Node Exporter + Grafana
- GitHub Actions

---

## 3. Configuración y entorno

1. Clonar el repositorio:
     ```bash
     git clone <URL_REPO>
     cd geopet-services
     ```

2. Variables de entorno (`.env`):
     - Claves de ImageKit:
         ```env
         PUBLIC_API_KEY="tu_public_api_key"
         PRIVATE_API_KEY="tu_private_api_key"
         ```
     - Credenciales de Firebase:
         - Colocar JSON en `credenciales/firebase-key.json`.
         - Convertir a base64:
             ```powershell
             [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("credenciales/firebase-key.json")) > firebase-key.b64.txt
             ```
         - Copiar el contenido de `firebase-key.b64.txt` a la variable `FIREBASE_KEY` del `.env`.

3. Entorno local:
     ```bash
     python -m venv venv
     source venv/bin/activate      # Linux/Mac
     # venv\Scripts\activate      # Windows
     pip install -r requirements.txt
     uvicorn main:app --reload
     ```

---

## 4. Scripts y pipelines

### 4.1 Scripts del pipeline / pruebas / despliegue

- `scripts/run_tests.sh`:
    ```bash
    ./scripts/run_tests.sh
    ```
    Compila todos los módulos de Python (chequeo sintáctico rápido).

- `scripts/build_image.sh`:
    ```bash
    ./scripts/build_image.sh
    ```
    Construye la imagen Docker `geopet-services` usando el `Dockerfile`.

- `scripts/run_local.sh`:
    ```bash
    ./scripts/run_local.sh
    ```
    Levanta la API localmente con `uvicorn main:app`.

- `scripts/deploy_docker.sh` (ejemplo):
    ```bash
    ./scripts/deploy_docker.sh
    ```
    Construye la imagen y deja comentado el push a un registry. Ajusta `<TU_REGISTRY>` según tu entorno.

### 4.2 GitHub Actions (CI/CD)

- `.github/workflows/test.yml` se ejecuta en cada push/PR y:
    - Instala dependencias.
    - Ejecuta una compilación de todos los archivos Python (chequeo rápido).

- `.github/workflows/deploy.yml` se ejecuta en push a `main` y:
    - Construye la imagen Docker.
    - La sube a GitHub Container Registry (`ghcr.io/<owner>/geopet-services:latest`).

---

## 5. Docker y entorno de liberación

### 5.1 Build de la imagen

```bash
docker build -t geopet-services .
```

### 5.2 Ejecutar la API con Docker

Usando el `.env` local:

```bash
docker run --rm -p 8000:8000 --env-file .env geopet-services
```

API docs:
- http://localhost:8000/docs

---

## 6. Monitoreo (Prometheus + Grafana)

### 6.1 Levantar stack de monitoreo

```bash
./scripts/start_monitoring.sh
```

Esto utiliza `docker-compose.monitoring.yml` para levantar:

- `app` (tu API FastAPI en `geopet-services`).
- `prometheus` leyendo `prometheus.yml` y `alerts.yml`.
- `node_exporter` para métricas del host.
- `grafana` para dashboards.

Puertos por defecto:

- API: http://localhost:8000
- Prometheus: http://localhost:9090
- Node Exporter: http://localhost:9100
- Grafana: http://localhost:3000

### 6.2 Configuración de Prometheus

`prometheus.yml` está configurado para scrapear:

- El propio Prometheus.
- La app en `/metrics` (ajusta si cambias el endpoint de métricas).
- Node Exporter.

---

## 7. Funcionalidades de la API

Embeddings (`/embedding`):

- `POST /embedding/generate` – Generar embedding de una imagen.
- `POST /embedding/generate_batch` – Generar embeddings de varias imágenes.
- `POST /embedding/compare` – Comparar imagen con mascotas perdidas.
- `POST /embedding/detect_species` – (No implementado aún).

ImageKit:

- `GET /imagekit-auth` – Obtener token de autenticación para cargas seguras.

Healthcheck:

- `GET /health` – Comprobar que la API está viva.

---

## 8. Licencia

EK'BALAM LICENSE