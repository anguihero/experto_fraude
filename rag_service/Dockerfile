# Usa una imagen ligera de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY . .

# Actualiza pip
RUN pip install --upgrade pip

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto del servicio (FastAPI escucha en 8000)
EXPOSE 8000

# Comando para lanzar el servicio
CMD ["python", "main.py"]