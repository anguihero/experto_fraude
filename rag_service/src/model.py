# rag_service/src/model.py

from pydantic import BaseModel

class ChatQuery(BaseModel):
    query: str  # Pregunta del usuario