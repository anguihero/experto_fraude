# api_gateway/src/routes.py

import logging
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import subprocess
import requests

# === CONFIGURACIÓN DE LOGGING ===

# Asegurar que el directorio de logs exista (importante al correr en contenedor)
os.makedirs("logs", exist_ok=True)

# Configurar el logger para escribir en archivo y consola
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/api_gateway.log"),  # Archivo persistente
        logging.StreamHandler()  # Consola (stdout)
    ]
)

logger = logging.getLogger(__name__)

# Crear instancia del router modular
router = APIRouter()

# === MODELOS DE DATOS ===

# Modelo para solicitudes de chat (envía un mensaje al modelo RAG)
class ChatRequest(BaseModel):
    message: str

# Modelo para autenticación (usuario y contraseña)
class AuthRequest(BaseModel):
    username: str
    password: str

# === ENDPOINT: /chat ===

@router.post("/chat", tags=["Chat"])
def chat(request: ChatRequest):
    """
    Recibe un mensaje del usuario y consulta al servicio RAG (/ask).
    Devuelve la respuesta del modelo.
    """
    logger.info(f"Solicitud de chat recibida: {request.message}")
    try:
        response = requests.post("http://rag_service:8001/ask", json={"query": request.message})
        response.raise_for_status()
        respuesta = response.json()["respuesta"]
        logger.info("Respuesta generada correctamente desde rag_service.")
        return {"respuesta": respuesta}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al consultar rag_service: {e}")
        raise HTTPException(status_code=500, detail=f"Error al consultar RAG: {str(e)}")

# === ENDPOINT: /actualizar-documentos ===

@router.post("/actualizar-documentos", tags=["Documentos"])
def actualizar_documentos():
    """
    Llama al servicio ingestion_service por HTTP para actualizar el índice FAISS.
    """
    logger.info("Solicitud para actualizar el índice FAISS.")
    try:
        # Se hace POST al endpoint del ingestion_service
        response = requests.post("http://ingestion_service:9000/update_index")
        response.raise_for_status()
        logger.info("Índice actualizado correctamente desde ingestion_service.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Fallo al consultar ingestion_service: {e}")
        raise HTTPException(status_code=500, detail=f"Error al actualizar documentos: {str(e)}")

# === ENDPOINT: /autenticar-usuario ===

@router.post("/autenticar-usuario", tags=["Autenticación"])
def autenticar_usuario(auth: AuthRequest):
    """
    Envia credenciales al microservicio auth_service para verificar autenticación.
    """
    logger.info(f"Solicitud de autenticación para el usuario: {auth.username}")
    try:
        response = requests.post("http://auth_service:9001/login", json=auth.dict())
        response.raise_for_status()
        logger.info("Autenticación exitosa.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error en autenticación: {e}")
        raise HTTPException(status_code=500, detail=f"Error en autenticación: {str(e)}")
