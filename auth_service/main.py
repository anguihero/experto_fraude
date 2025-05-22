from fastapi import FastAPI
from src.routes import router
from src.logger import setup_logger

app = FastAPI(
    title="Auth Service - Verificación de Usuarios",
    version="1.0"
)

app.include_router(router)

setup_logger()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9001)
