# rag_service/src/routes.py

from fastapi import APIRouter
from src.model import ChatQuery
from src.chains import qa_chain, chat_history
import logging

# Configurar router de FastAPI
router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/ask", tags=["Chat"])
def responder_pregunta(payload: ChatQuery):
    """
    Endpoint para recibir preguntas y devolver respuestas desde el modelo RAG.
    
    Requiere:
    - query: string con la pregunta

    Retorna:
    - respuesta generada por el modelo
    """
    pregunta = payload.query
    logger.info(f"Consulta recibida: {pregunta}")

    try:
        respuesta = qa_chain.run({"question": pregunta, "chat_history": chat_history})
        chat_history.append((pregunta, respuesta))
        logger.info("Respuesta generada exitosamente.")
        return {"respuesta": respuesta}
    except Exception as e:
        logger.exception("Error durante la generación de respuesta.")
        return {"error": str(e)}
