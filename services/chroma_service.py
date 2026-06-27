import os
import chromadb
from chromadb.config import Settings
from services.embedding_service import create_embedding

CHROMA_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

client = chromadb.PersistentClient(
    path=CHROMA_PATH,
    settings=Settings(anonymized_telemetry=False)
)

def get_collection():


    return client.get_or_create_collection(
        name="pdf_chunks"
    )

def store_chunks(chunks, pdf_name):

    collection = get_collection()

    existing_ids = collection.get()["ids"]

    if existing_ids:
        collection.delete(ids=existing_ids)

    print("Total Chunks:", collection.count())

    ids = [str(i) for i in range(len(chunks))]

    metadatas = [
        {"source": pdf_name}
        for _ in chunks
    ]

    embeddings = [create_embedding(chunk) for chunk in chunks]
    
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print("Total Chunks:", collection.count())

    return collection

def search_chunks(question, n_results=8):

    collection = client.get_collection(
        name="pdf_chunks"
    )
    embedding = create_embedding(question)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    print("Question:", question)
    print("Retrieved Chunks:", len(results["documents"][0]))
    return results

def get_count():
    collection = get_collection()
    return collection.count()