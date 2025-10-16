from services.mobile_net_loader import embedding_model
from fastapi import APIRouter,UploadFile, File
from services.embedding_utils import generar_embedding_desde_bytes, generar_embeddings_desde_bytes_list
from services.firebase_utils import obtener_mascotas_perdidas
from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from typing import List
from datetime import datetime
from scipy.spatial.distance import cosine


vision_router = APIRouter(prefix = "/embedding", tags = ["Embeddings"])


@vision_router.post("/detect_species")
def detectar_especies():
    return None

#Ruta para la obtencion de los embedding individual
#Genera embedding de la imagen usando MobileNetV2
@vision_router.post("/generate")
async def generar_embedding(image: UploadFile = File(...)):
    img_bytes = await image.read()
    emb = await run_in_threadpool(generar_embedding_desde_bytes, img_bytes, embedding_model)
    if emb is None:
        raise HTTPException(status_code=500, detail="Error al generar el embedding")
    return {"embedding": emb.tolist(), "dim": emb.shape[0]}


# Batch (varias imágenes en una sola request)
@vision_router.post("/generate_batch")
async def generar_embeddings(images: List[UploadFile] = File(...)):
    # lee bytes
    imgs_bytes = [await f.read() for f in images]   
    embs = await run_in_threadpool(generar_embeddings_desde_bytes_list, imgs_bytes, embedding_model)
    if embs is None:
        raise HTTPException(status_code=500, detail="Error al generar embeddings en batch")
    created_at = datetime.now().isoformat()
    return {
        "embeddings": [e.tolist() for e in embs], 
        "count": len(embs), 
        "dim": embs.shape[1],
        "created_at": created_at
        }

# Comparar dos imágenes (devuelve similitud cosine)
@vision_router.post("/compare")
async def comparar_embbedding(image: UploadFile = File(...)):
    #Se lee la imagen enviada desde la app movil
    image_bytes = await image.read()
    #Se procesa para la generacion de embeddings
    embedding = await run_in_threadpool(generar_embedding_desde_bytes, image_bytes, embedding_model)
    if embedding is None:
        raise HTTPException(status_code=500, detail="Error al generar el embedding")   
     
    mascotas = obtener_mascotas_perdidas()
    resultados = []
    for mascota in mascotas:
        fotos = mascota.get('fotosMascota',[])
        scores = []
        for foto in fotos:
            emb = foto.get('embedding')
            if emb:
                sim = 1 - cosine(embedding, emb)
                scores.append(sim)
                
        if scores:
            avg_sim = sum(scores) / len(scores)
            if avg_sim >= 0.55:
                resultados.append({
                    'idMascota': mascota['idMascota'],
                    'score': avg_sim
                })   
    
    resultados.sort(key=lambda x: x['score'], reverse=True)
    return {"resultados": resultados}



