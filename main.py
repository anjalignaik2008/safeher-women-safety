from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="SafeHer - Women Safety Support System", version="1.0.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# In-memory demo storage. Records reset when the server restarts.
activity = []

class SOSRequest(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CheckinRequest(BaseModel):
    name: str = Field(default="", max_length=80)

class IncidentRequest(BaseModel):
    category: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=2000)
    location: str = Field(default="", max_length=250)


def add_activity(kind: str, message: str, details: Optional[dict] = None):
    record = {
        "id": str(uuid4())[:8],
        "type": kind,
        "message": message,
        "details": details or {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    activity.insert(0, record)
    del activity[100:]
    return record


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "SafeHer"}


@app.post("/api/sos")
def create_sos(payload: SOSRequest):
    details = {}
    if payload.latitude is not None and payload.longitude is not None:
        details = {"latitude": payload.latitude, "longitude": payload.longitude}
    record = add_activity("SOS", "Demo SOS alert recorded", details)
    return {"ok": True, "message": "Demo SOS alert recorded. No emergency services were contacted.", "record": record}


@app.post("/api/checkin")
def checkin(payload: CheckinRequest):
    name = payload.name.strip()
    message = f"{name or 'User'} checked in as safe"
    record = add_activity("Check-in", message, {"name": name})
    return {"ok": True, "message": "Safety check-in recorded.", "record": record}


@app.post("/api/incidents")
def report_incident(payload: IncidentRequest):
    category = payload.category.strip()
    description = payload.description.strip()
    if not category or not description:
        raise HTTPException(status_code=400, detail="Category and description are required.")
    record = add_activity(
        "Incident",
        f"{category} incident reported",
        {"category": category, "description": description, "location": payload.location.strip()},
    )
    return {"ok": True, "message": "Incident report recorded in this demo.", "record": record}


@app.get("/api/history")
def get_history():
    return {"items": activity}
