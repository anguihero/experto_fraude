# api_gateway/main.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from src.routes import router as app_router

# Middleware para habilitar CORS
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permitir todos los orígenes (ajusta si necesitas seguridad)
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

# Configuración principal de FastAPI
app = FastAPI(
    title="Chatbot Experto en Fraude",
    description="API gateway para interacción con el sistema de RAG, autenticación de usuarios y actualización de documentos.",
    version="1.0.0",
    openapi_url="/experto_fraude/openapi.json",
    docs_url="/experto_fraude/docs",
    middleware=middleware,
)

# Registrar el router principal
app.include_router(app_router)

# Punto de entrada para ejecución directa
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
