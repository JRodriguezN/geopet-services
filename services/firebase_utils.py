import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('credenciales/firebase-key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def obtener_mascotas_perdidas():
    mascotas_ref = db.collection('mascotas')
    query = mascotas_ref.where('estaPerdida', '==', True)
    docs = query.stream()
    mascotas = []
    for doc in docs:
        data = doc.to_dict()
        data['idMascota'] = doc.id
        mascotas.append(data)
    return mascotas