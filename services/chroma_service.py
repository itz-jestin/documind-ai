import os
import chromadb
from chromadb.config import Settings
from services.embedding_service import create_embedding
import time

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

    start = time.time()
    collection = get_collection()
    print("Get collection:", time.time() - start)

    start = time.time()
    existing_ids = collection.get()["ids"]
    print("Get existing ids:", time.time() - start)

    if existing_ids:
        start = time.time()
        collection.delete(ids=existing_ids)
        print("Delete:", time.time() - start)

    ids = [str(i) for i in range(len(chunks))]
    metadatas = [{"source": pdf_name} for _ in chunks]

    start = time.time()
    embeddings = create_embedding(chunks)
    print("Embedding:", time.time() - start)

    start = time.time()
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )
    print("Add to Chroma:", time.time() - start)

    return collection

def search_chunks(question, n_results=5):

    collection = get_collection()
    start = time.perf_counter()
    embedding = create_embedding(question)
    print("Embedding:", time.perf_counter() - start)
    
    start = time.perf_counter()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=n_results
    )
    print("Query:", time.perf_counter() - start)
    print("Question:", question)
    print("Retrieved Chunks:", len(results["documents"][0]))
    return results

def get_count():
    collection = get_collection()
    return collection.count()