from tensorflow.keras.applications import MobileNetV2

# Cargar modelo IMAGENET para obtener embeddings
embedding_model = MobileNetV2(weights='imagenet', include_top=False, pooling='avg')