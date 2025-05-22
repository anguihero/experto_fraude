# ingestion_service/main.py

from fastapi import FastAPI
from src.routes import router as ingestion_router

app = FastAPI(
    title="Servicio de Ingesta RAG",
    description="Microservicio para vectorizar documentos y actualizar el índice FAISS.",
    version="1.0.0"
)

app.include_router(ingestion_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=9000)
