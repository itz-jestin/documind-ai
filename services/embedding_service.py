from sentence_transformers import SentenceTransformer
import time

start = time.perf_counter()
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded in:", time.perf_counter() - start)

def create_embedding(texts):
    start = time.perf_counter()

    embeddings = model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True
    )

    print("Encoding took:", time.perf_counter() - start)

    return embeddings.tolist()