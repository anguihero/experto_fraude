# Importaciones estándar y módulos internos
import os
import logging
from fastapi import APIRouter, HTTPException, Header
from src.models import AuthRequest, RegistroRequest
from src.database import verificar_usuario, obtener_usernames, registrar_usuario

# Inicialización del logger para trazabilidad
logger = logging.getLogger(__name__)

# Cargar la clave maestra desde .env o usar un valor por defecto (por seguridad solo para entorno local)
MASTER_KEY = os.getenv("MASTER_KEY", "default_master_key")

# Crear instancia del router que luego se añade a la app FastAPI
router = APIRouter()

# =====================================================
# ENDPOINT: POST /login
# =====================================================
@router.post("/login", tags=["Autenticación"])
def login(data: AuthRequest):
    """
    Verifica si el usuario y la contraseña ingresados coinciden con
    un registro en la base de datos SQLite.

    Parámetros:
    - data (AuthRequest): JSON con `username` y `password`

    Retorna:
    - 200 OK si es exitoso
    - 401 Unauthorized si falla
    """
    logger.info(f"Intento de autenticación de usuario: {data.username}")
    if verificar_usuario(data.username, data.password):
        logger.info("Autenticación exitosa")
        return {"status": "ok", "message": "Usuario autenticado"}
    else:
        logger.warning("Fallo de autenticación")
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")


# =====================================================
# ENDPOINT: GET /usuarios
# =====================================================
@router.get("/usuarios", tags=["Administración"])
def listar_usuarios(x_admin_key: str = Header(..., alias="X-Admin-Key")):
    """
    Devuelve la lista de usernames registrados, sin contraseñas.

    Requiere header:
    - X-Admin-Key: Clave maestra definida en .env (MASTER_KEY)

    Retorna:
    - 200 OK con lista de usuarios
    - 403 Forbidden si la clave es incorrecta
    """
    logger.info("Solicitud recibida para obtener lista de usuarios")

    if x_admin_key != MASTER_KEY:
        logger.warning("Intento no autorizado a /usuarios")
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

    try:
        usuarios = obtener_usernames()
        logger.info(f"{len(usuarios)} usuarios recuperados")
        return {"usuarios": usuarios}
    except Exception as e:
        logger.error(f"Error al recuperar usuarios: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


# =====================================================
# ENDPOINT: POST /registro
# =====================================================
@router.post("/registro", tags=["Administración"])
def registrar_usuario_endpoint(
    data: RegistroRequest,
    x_admin_key: str = Header(..., alias="X-Admin-Key")
):
    """
    Registra un nuevo usuario en la base de datos.

    Requiere:
    - JSON con username y password (mínimo 6 caracteres)
    - Header X-Admin-Key con la clave maestra

    Retorna:
    - 201 Created si el usuario fue creado
    - 409 Conflict si ya existe
    - 403 Forbidden si la clave es incorrecta
    """
    logger.info(f"Solicitud de registro para nuevo usuario: {data.username}")

    if x_admin_key != MASTER_KEY:
        logger.warning("Intento de registro no autorizado")
        raise HTTPException(status_code=403, detail="Acceso no autorizado")

    if len(data.password) < 6:
        logger.warning("Contraseña demasiado corta")
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")

    exito = registrar_usuario(data.username, data.password)
    if exito:
        logger.info(f"Usuario '{data.username}' registrado exitosamente")
        return {"status": "ok", "message": f"Usuario '{data.username}' registrado correctamente"}
    else:
        logger.warning(f"Usuario ya existente: {data.username}")
        raise HTTPException(status_code=409, detail="El usuario ya existe")
