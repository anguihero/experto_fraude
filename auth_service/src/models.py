# src/models.py

from pydantic import BaseModel, Field

# =====================================================
# Modelo para solicitudes de autenticación (login)
# =====================================================
class AuthRequest(BaseModel):
    """
    Modelo para validar el payload de autenticación.
    """
    username: str = Field(..., example="usuario")
    password: str = Field(..., example="987654")


# =====================================================
# Modelo para solicitudes de registro de nuevos usuarios
# =====================================================
class RegistroRequest(BaseModel):
    """
    Modelo para validar el payload de registro.
    """
    username: str = Field(..., min_length=3, example="nuevo_usuario")
    password: str = Field(..., min_length=6, example="contraseña_segura")
