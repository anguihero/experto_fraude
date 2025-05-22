#!/bin/bash

echo "🔁 Deteniendo contenedores existentes..."
docker-compose down

echo "🧹 Eliminando contenedores detenidos, redes y volúmenes huérfanos..."
docker system prune -f

echo "🚨 (Opcional) Eliminando imágenes anteriores del proyecto..."
docker rmi $(docker images | grep 'ingestion_service\|rag_service\|api_gateway' | awk '{print $3}') -f 2>/dev/null

echo "📦 Reconstruyendo imágenes y contenedores..."
docker-compose build --no-cache

echo "🚀 Levantando el stack completo..."
docker-compose up -d

echo "✅ Listo. Accede a los servicios:"
echo "🔹 API Gateway:       http://localhost:8000"
echo "🔹 Servicio RAG:      http://localhost:8001"
echo "🔹 Ingesta documentos: http://localhost:9000/docs"
