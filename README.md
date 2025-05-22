# Fraud Expert Chatbot using RAG + FastAPI + Gemini

This project implements a **fraud-focused AI chatbot**, combining:

- **RAG (Retrieval-Augmented Generation)** with vectorized documents via FAISS.
- **Gemini API (Google Generative AI)** as the language model.
- **FastAPI** for building a clean RESTful interface.
- **SQLite** for user authentication.
- **Docker Compose** for modular microservice orchestration.

---

## 🎯 Project Purpose

To develop an **intelligent conversational assistant** that:

- Answers questions based on fraud-related documentation.
- Maintains **contextual conversation history**.
- Allows **dynamic knowledge updates** through document ingestion.
- Uses secure authentication via API.
- Is **modular, containerized, and production-ready**.

---


## System Architecture

```
┌──────────────────────────┐ ┌──────────────────────────────┐
│ DOCUMENTACION_FRAUDE │────▶ │ ingestion_service │
└──────────────────────────┘ │ - Vectorizes docs (FAISS) │
└────────────┬─────────────────┘
▼
┌──────────────────────────────────┐
│ rag_service │
│ - LangChain + Gemini 2.0 Flash │
└────────────┬─────────────────────┘
▼
┌────────────────────┐ ┌──────────────────────────────────┐
│ auth_service │────▶ │ api_gateway │
│ - Verifies users │ │ - /chat /update /login endpoints │
└────────────────────┘ └──────────────────────────────────┘
```

---

## Project Structure

```
experto_fraude/
├── api_gateway/
│ ├── main.py
│ ├── src/
│ ├── Dockerfile
│ └── requirements.txt
├── auth_service/
│ ├── main.py
│ ├── src/
│ ├── usuarios.db
│ ├── Dockerfile
│ └── requirements.txt
├── ingestion_service/
│ ├── main.py
│ ├── src/
│ ├── faiss_index/
│ ├── DOCUMENTACION_FRAUDE/
│ ├── Dockerfile
│ └── requirements.txt
├── rag_service/
│ ├── main.py
│ ├── src/
│ ├── Dockerfile
│ └── requirements.txt
├── logs/
├── docker-compose.yml
├── build.sh
├── init_db.py
├── notas_desarrollo.txt
└── README.md
```

---


---

## Services and API Endpoints

| Service          | Port  | Purpose                                 | Endpoints                                  |
|------------------|--------|-----------------------------------------|--------------------------------------------|
| `api_gateway`     | 8000   | Handles all public endpoints            | `/chat`, `/actualizar-documentos`, `/login`|
| `rag_service`     | 8001   | Responds using Gemini + FAISS index     | `/ask`                                     |
| `ingestion_service` | 9000 | Indexes documents and updates FAISS     | `/actualizar`, `/estado`                   |
| `auth_service`    | 9001   | Manages authentication and users        | `/login`, `/usuarios`, `/registro`         |

---

## Deployment Guide

1. **Clone this repository**
2. **Place your documents** under `ingestion_service/DOCUMENTACION_FRAUDE/`
3. **Set up `.env` files** for Gemini API and Admin access:

### `rag_service/.env` and `ingestion_service/.env`
```env
GOOGLE_API_KEY=your_google_api_key
```


Access the APIs:

1. http://localhost:8000/docs (Main API)
2. http://localhost:9000/docs (Ingestion RAG)
3. http://localhost:9001/docs (Auth)
4. http://localhost:8001/docs (Ask)

## Example Chat Request

* POST http://localhost:8000/chat:

```
{  
  "message": "How can I detect internal fraud?"
  }
```

* Response:
```
{  
  "respuesta": "Internal fraud refers to acts committed by employees..."
  }
```

## Security & Authorization

* Endpoints /usuarios and /registro require the X-Admin-Key header.
* Passwords are never exposed through any endpoint.
* SQLite is used for easy deployment and testing.

## Recent Technical Updates

* Migrated to gemini-2.0-flash model (via langchain-google-genai).
* Refactored to 4 independent microservices.
* Added user login, registration and admin listing.
* Full persistent FAISS index sharing across containers.
* Logging to separate folders for each service.

##  Expansion Possibilities

1. Web frontend (React, Vue, etc.) for chat UI.
2. Integration with WhatsApp, Slack, Telegram.
3. Citation-based answers with references.
4. Admin dashboard to monitor interactions and retrain.