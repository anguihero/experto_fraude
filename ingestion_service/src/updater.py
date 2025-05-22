# ingestion_service/src/updater.py

import os
import glob
import logging
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import csv
from datetime import datetime
from typing import List, Dict

load_dotenv()
logger = logging.getLogger(__name__)

def registrar_auditoria(documentos: list, log_path: str = "logs/index_auditoria.csv"):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    existe = os.path.exists(log_path)

    with open(log_path, mode="a", newline="", encoding="utf-8") as archivo:
        writer = csv.writer(archivo)
        if not existe:
            writer.writerow(["nombre_archivo", "longitud_contenido", "fecha_indexado"])
        
        for doc in documentos:
            nombre = doc.metadata.get("source", "desconocido")
            contenido = doc.page_content.strip()
            fecha = datetime.now().isoformat()
            writer.writerow([nombre, len(contenido), fecha])

def actualizar_indice():
    # Validar API Key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY no está definida")

    # Embedding y configuración
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # Cargar documentos
    documentos = []
    loader_txt = DirectoryLoader("DOCUMENTACION_FRAUDE", glob="*.txt")
    documentos.extend(loader_txt.load())

    for ruta in glob.glob("DOCUMENTACION_FRAUDE/*.pdf"):
        documentos.extend(PyPDFLoader(ruta).load())

    for ruta in glob.glob("DOCUMENTACION_FRAUDE/*.docx"):
        documentos.extend(UnstructuredFileLoader(ruta).load())

    logger.info(f"{len(documentos)} documentos cargados")

    # Eliminar vacíos y duplicados
    texto_visto = set()
    documentos_filtrados = []

    for doc in documentos:
        contenido = doc.page_content.strip()
        if contenido and contenido not in texto_visto:
            documentos_filtrados.append(doc)
            texto_visto.add(contenido)

    logger.info(f"{len(documentos_filtrados)} documentos filtrados (sin vacíos ni duplicados)")

    if not documentos_filtrados:
        raise ValueError("No hay documentos válidos para indexar")

    # Fragmentar documentos
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    partes = splitter.split_documents(documentos_filtrados)

    # Ruta del índice persistente
    INDEX_PATH = "faiss_index"
    os.makedirs(INDEX_PATH, exist_ok=True)

    # Crear o cargar índice
    if os.path.exists(f"{INDEX_PATH}/index.faiss"):
        db = FAISS.load_local(INDEX_PATH, embedding, allow_dangerous_deserialization=True)
        db.add_documents(partes)
        logger.info("Índice existente cargado y extendido.")
    else:
        db = FAISS.from_documents(partes, embedding)
        logger.info("Índice nuevo creado.")

    db.save_local(INDEX_PATH)
    registrar_auditoria(documentos_filtrados)
    logger.info("Auditoría de documentos registrada en logs/index_auditoria.csv")
    return {"documentos": len(documentos), "partes": len(partes)}

def obtener_estado_indice():
    """
    Retorna el número de documentos y fragmentos del índice si existe.
    """
    INDEX_PATH = "faiss_index"
    if not os.path.exists(f"{INDEX_PATH}/index.faiss"):
        raise FileNotFoundError("El índice FAISS no ha sido creado aún.")

    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = FAISS.load_local(INDEX_PATH, embedding, allow_dangerous_deserialization=True)
    
    return {
        "documentos_indexados": len(db.docstore._dict),  # número de documentos
        "ruta": INDEX_PATH
    }

def leer_auditoria_csv(log_path: str = "logs/index_auditoria.csv", n: int = 10) -> List[Dict]:
    """
    Retorna las últimas N filas del archivo de auditoría como lista de diccionarios.
    """
    if not os.path.exists(log_path):
        return []

    with open(log_path, mode="r", encoding="utf-8") as archivo:
        lector = list(csv.DictReader(archivo))
        return lector[-n:] if len(lector) >= n else lector