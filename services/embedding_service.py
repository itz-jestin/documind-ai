import time
from sentence_transformers import SentenceTransformer

start=time.time()
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded in:", time.time() - start)

def create_embeddings(texts):
    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True
    ).tolist()