# rag_service/main.py
from fastapi import FastAPI
from src.routes import router
from src.logger import setup_logger

# Crear la aplicación FastAPI
app = FastAPI(
    title="RAG Service - Chatbot Experto en Fraude",
    description="Servicio que responde preguntas usando recuperación de contexto con Gemini + FAISS",
    version="1.0"
)

# Incluir el router definido en src/routes.py
app.include_router(router)

# Ejecutar el servidor si se lanza directamente
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
