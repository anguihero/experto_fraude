# src/chains.py

import os
import logging
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Configura logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Validar que la clave API esté presente
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise EnvironmentError("Falta la variable GOOGLE_API_KEY en el entorno.")

# Inicializar modelo de embedding
embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Cargar índice FAISS persistente
INDEX_PATH = "faiss_index"
if not os.path.exists(f"{INDEX_PATH}/index.faiss"):
    raise FileNotFoundError(f"No se encontró el índice FAISS en {INDEX_PATH}/index.faiss. Verifica que se haya generado correctamente.")

# Cargar el índice vectorial
retriever = FAISS.load_local(
    INDEX_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
).as_retriever()
logger.info("Índice FAISS cargado correctamente.")

# Inicializar modelo Gemini con opción para convertir SystemMessage a HumanMessage
llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    temperature=0.3,
    convert_system_message_to_human=True  # <- evita el error de SystemMessage no soportado
)

# Crear la cadena de recuperación conversacional
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever
)

# Inicializar historial de chat (puede compartirse entre solicitudes)
chat_history = []
