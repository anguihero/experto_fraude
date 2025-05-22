FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia todos los archivos al contenedor
COPY . .

# Actualiza pip y setuptools antes de instalar requirements
RUN pip install --upgrade pip setuptools
# Instala dependencias sin usar caché
RUN pip install --no-cache-dir -r requirements.txt

# (Opcional) Descarga recursos de NLTK como 'punkt'
RUN python -m nltk.downloader punkt

# Lanza la aplicación FastAPI con Uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
