# src/database.py

import sqlite3
import logging
from typing import List

# Ruta a la base de datos SQLite
DB_PATH = "usuarios.db"

# Configuración básica de logging
logger = logging.getLogger(__name__)

def conectar_db() -> sqlite3.Connection:
    """
    Abre una conexión a la base de datos SQLite.
    """
    return sqlite3.connect(DB_PATH)

def verificar_usuario(username: str, password: str) -> bool:
    """
    Verifica si el usuario y la contraseña coinciden con un registro existente.

    Args:
        username (str): Nombre de usuario.
        password (str): Contraseña del usuario.

    Returns:
        bool: True si existe coincidencia, False en caso contrario.
    """
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE username=? AND password=?", (username, password))
        resultado = cursor.fetchone()
        return resultado is not None
    except Exception as e:
        logger.error(f"Error al verificar usuario: {e}")
        return False
    finally:
        conn.close()

def registrar_usuario(username: str, password: str) -> bool:
    """
    Registra un nuevo usuario en la base de datos.

    Args:
        username (str): Nuevo nombre de usuario.
        password (str): Contraseña del nuevo usuario.

    Returns:
        bool: True si fue registrado exitosamente, False si ya existe o hay error.
    """
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"Usuario ya existente: {username}")
        return False
    except Exception as e:
        logger.error(f"Error al registrar usuario: {e}")
        return False
    finally:
        conn.close()

def obtener_usernames() -> List[str]:
    """
    Retorna una lista con todos los nombres de usuario registrados (sin contraseñas).

    Returns:
        List[str]: Lista de usernames existentes.
    """
    try:
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM usuarios")
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception as e:
        logger.error(f"Error al obtener usuarios: {e}")
        return []
    finally:
        conn.close()
