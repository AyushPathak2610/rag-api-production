# from fastapi import FastAPI
# import chromadb
# import ollama

# app = FastAPI()
# chroma = chromadb.PersistentClient(path="./db")
# collection = chroma.get_or_create_collection("docs")
# # ollama_client = ollama.Client(host="http://host.docker.internal:11434") # kubernetes
# # ollama_client = ollama.Client(host="http://ollama-server:11434") # docker-compose
# ollama_client = ollama.Client(host="http://localhost:11434") # local

# @app.post("/query")
# def query(q: str):
#     results = collection.query(query_texts=[q], n_results=1)

#     context = ""
#     if results.get("documents") and len(results["documents"]) > 0:
#         context = results["documents"][0][0]

#     answer = ollama_client.generate(
#         model="tinyllama",
#         prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
#     )

#     return {"answer": answer["response"]}

# @app.post("/add")
# def add_knowledge(text: str):
#     """Add new content to the knowledge base dynamically."""
#     try:
#         # Generate a unique ID for this document
#         import uuid
#         doc_id = str(uuid.uuid4())
        
#         # Add the text to Chroma collection
#         collection.add(documents=[text], ids=[doc_id])
        
#         return {
#             "status": "success",
#             "message": "Content added to knowledge base",
#             "id": doc_id
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e)
#         }



import os
from fastapi import FastAPI
import chromadb

# Mock LLM mode for CI testing
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "0") == "1"

if not USE_MOCK_LLM:
    import ollama

app = FastAPI()
chroma = chromadb.PersistentClient(path="./db")
collection = chroma.get_or_create_collection("docs")

@app.post("/query")
def query(q: str):
    results = collection.query(query_texts=[q], n_results=1)
    context = results["documents"][0][0] if results["documents"] else ""

    if USE_MOCK_LLM:
        # In mock mode, return the retrieved context directly
        return {"answer": context}

    # In production mode, use Ollama
    answer = ollama.generate(
        model="tinyllama",
        prompt=f"Context:\n{context}\n\nQuestion: {q}\n\nAnswer clearly and concisely:"
    )

    return {"answer": answer["response"]}
