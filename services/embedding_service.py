from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(texts):
    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True
    ).tolist()