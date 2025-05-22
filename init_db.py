import sqlite3


# Conectar a la base de datos (se crea si no existe)
conn = sqlite3.connect("auth_service/usuarios.db")
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# Insertar usuarios por defecto (no se duplican si ya existen)
usuarios_por_defecto = [
    ("admin", "123456"),
    ("sysadmin", "987654")
]

for username, password in usuarios_por_defecto:
    cursor.execute(
        "INSERT OR IGNORE INTO usuarios (username, password) VALUES (?, ?)",
        (username, password)
    )

# Confirmar y cerrar
conn.commit()
conn.close()
print("Base de datos inicializada con usuarios por defecto.")

