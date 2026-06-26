from fastapi import FastAPI,UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.pdf_service import extract_pdf_text
from services.chunking_service import split_by_sentences
from services.chroma_service import store_chunks, search_chunks ,get_count
from models import QuestionRequest
from services.llm_service import ask_llm
from pypdf import PdfReader
import os
import time


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
pdf_text = ""


@app.get("/")
def home():
    return {"message": "PDF text extractor API!"}

start = time.time()
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    upload_start = time.time()
    global pdf_text
    
    # Save uploaded pdf
    
    file_path=f"uploads/{file.filename}"  #example: uploads/sample.pdf

    with open(file_path, "wb") as f:  #wb means write binary mode
        content = await file.read()
        f.write(content)

    # Read PDF 

    start=time.time()
    text = extract_pdf_text(file_path)
    print("PDF Extraction Time:", time.time() - start)  

    start=time.time()
    chunks = split_by_sentences(text,sentences_per_chunk=4)
    print("Chunking Time:", time.time() - start)

    start=time.time()
    store_chunks(chunks,file.filename)
    print("Chroma Store:",time.time() - start)
    pdf_text=text

    reader =PdfReader(file_path)
    print("Upload Time:", time.time() - upload_start)
    return {
    "filename": file.filename,
    "pages": len(reader.pages),
    "characters": len(text),
    "preview": text[:500]
}
start = time.time()
@app.post("/ask-pdf")
async def ask_pdf(data: QuestionRequest):

    global pdf_text

    if not pdf_text:
        return {
            "error": "Please upload a PDF first."
        }
    start=time.time()
    results = search_chunks(data.question,n_results=3)
    print("Search Time:", time.time() - start)
    for i, chunk in enumerate(results["documents"][0], start=1):
       print(f"\nChunk {i}:")
       print(chunk[:300])

    print("\nSources:")
    print(results["metadatas"][0])
    chunks=results["documents"][0]
    context = "\n\n".join(
    [f"Chunk {i+1}:\n{chunk}"
     for i, chunk in enumerate(chunks)])

    print(results["metadatas"])
    print("Total Chunks:", get_count())
    start=time.time()
    answer = ask_llm(
        context,
        data.question
    )
    print("Answer Time:", time.time() - start)
    
    return {
        "question": data.question,
        "retrieved_chunks": results["documents"][0],
        "sources": results["metadatas"][0],
        "answer": answer,
    }