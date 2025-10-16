from PIL import Image
import io
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

def _preprocess_bytes(image_bytes: bytes):
    pil = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(pil, dtype=np.float32)
    return arr

def generar_embedding_desde_bytes(image_bytes: bytes, model):
    try:
        arr = _preprocess_bytes(image_bytes)
        x = np.expand_dims(arr, axis=0)
        x = preprocess_input(x)
        emb = model.predict(x, verbose=0)[0].astype(np.float32)
        norm = np.linalg.norm(emb)
        if norm > 0:
            emb = emb / norm
        return emb
    except Exception as e:
        return None
    
def generar_embeddings_desde_bytes_list(image_bytes_list: list, model):
    """
    Batch predict: recibe lista de bytes, devuelve array (N, D) normalizado.
    """
    try:
        arrs = [ _preprocess_bytes(b) for b in image_bytes_list ]
        X = np.stack(arrs, axis=0)
        X = preprocess_input(X)
        embs = model.predict(X, verbose=0).astype(np.float32)
        norms = np.linalg.norm(embs, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-10)
        embs = embs / norms
        return embs
    except Exception as e:
        return None