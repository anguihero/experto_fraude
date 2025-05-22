from fastapi import APIRouter, HTTPException, Query
from src.updater import actualizar_indice, obtener_estado_indice, leer_auditoria_csv
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/update_index", tags=["Actualización"])
def update_index_endpoint():
    """
    Actualiza el índice FAISS con nuevos documentos.
    """
    try:
        resultado = actualizar_indice()
        return {"mensaje": "Índice actualizado correctamente", "detalles": resultado}
    except Exception as e:
        logger.error(f"Error actualizando índice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status_index", tags=["Estado"])
def status_index_endpoint():
    """
    Devuelve el estado actual del índice FAISS si existe.
    """
    try:
        estado = obtener_estado_indice()
        return {"estado": estado}
    except Exception as e:
        logger.error(f"Error al obtener estado del índice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/auditoria", tags=["Auditoría"])
def obtener_auditoria(n: int = Query(10, description="Número de entradas a mostrar")):
    """
    Devuelve las últimas N entradas del registro de auditoría de documentos indexados.
    """
    try:
        registros = leer_auditoria_csv(n=n)
        return {"auditoria": registros}
    except Exception as e:
        logger.error(f"Error al leer auditoría: {e}")
        raise HTTPException(status_code=500, detail=str(e))