# Texto Contador App

Aplicación fullstack: página web con botón para guardar texto y mostrar contador de palabras/caracteres.

## Stack
- **Backend:** FastAPI + Firestore
- **Frontend:** HTML/CSS/JS + nginx

## Acceso local
```bash
docker compose up -d
# Frontend: http://localhost:8092
# Backend:  http://localhost:8091
```

## Variables de entorno (backend)
```
FIRESTORE_PROJECT_ID=openclawbotvic
FIRESTORE_COLLECTION=texto-contador-app
KAISER_WEBHOOK_TOKEN=<token>
GOOGLE_CREDENTIALS_JSON=<json>
```
