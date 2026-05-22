import json
import os
from datetime import datetime

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI
from google.cloud import firestore
from google.oauth2 import service_account
from pydantic import BaseModel

load_dotenv()

FIRESTORE_PROJECT_ID = os.getenv("FIRESTORE_PROJECT_ID", "openclawbotvic")
FIRESTORE_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "text-counter-api")
KAISER_WEBHOOK_TOKEN = os.getenv("KAISER_WEBHOOK_TOKEN", "")
KAISER_ANALYTICS_URL = os.getenv(
    "KAISER_ANALYTICS_URL",
    "https://kaiser.vicdata.co/api/v1/tech/analytics/event",
)
APP_WORKSPACE = "text-counter-api"

# Soporte para credenciales inyectadas como JSON string (DevOps platform / Secret Manager)
_gcp_creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
if _gcp_creds_json:
    _sa_info = json.loads(_gcp_creds_json)
    _credentials = service_account.Credentials.from_service_account_info(
        _sa_info,
        scopes=["https://www.googleapis.com/auth/datastore"],
    )
    db = firestore.Client(project=FIRESTORE_PROJECT_ID, credentials=_credentials)
else:
    db = firestore.Client(project=FIRESTORE_PROJECT_ID)


async def track_event(
    event_type: str,
    entity_id: str = None,
    entity_type: str = None,
    properties: dict = None,
) -> None:
    try:
        async with httpx.AsyncClient(timeout=3) as client:
            await client.post(
                KAISER_ANALYTICS_URL,
                json={
                    "app_workspace": APP_WORKSPACE,
                    "event_type": event_type,
                    "entity_id": entity_id,
                    "entity_type": entity_type,
                    "properties": properties or {},
                },
                headers={"X-Internal-Token": KAISER_WEBHOOK_TOKEN},
            )
    except Exception:
        pass


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Text Counter API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TextRequest(BaseModel):
    text: str


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/count")
async def count_text(request: TextRequest):
    word_count = len(request.text.split()) if request.text.strip() else 0
    char_count = len(request.text)

    data = {
        "text": request.text,
        "word_count": word_count,
        "char_count": char_count,
        "timestamp": datetime.utcnow(),
    }

    _, doc_ref = db.collection(FIRESTORE_COLLECTION).add(data)
    document_id = doc_ref.id

    await track_event(
        "text_analyzed",
        entity_type="text_analysis",
        entity_id=document_id,
        properties={"word_count": word_count, "char_count": char_count},
    )

    return {"word_count": word_count, "char_count": char_count, "doc_id": document_id}
