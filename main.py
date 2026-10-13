import logging, platform, shutil
from collections import deque
from threading import Lock
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.config import settings
from app.metrics import build_event, calculate_metrics

logging.basicConfig(level=getattr(logging, settings.log_level, logging.INFO),
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(settings.service_name)
app = FastAPI(title="Cloud Service Health Monitor", version="1.0.0")
EVENTS = deque(maxlen=settings.max_events)
LOCK = Lock()

class EventRequest(BaseModel):
    severity: str
    component: str = Field(..., min_length=1)
    latency_ms: float = Field(..., ge=0)
    success: bool

@app.get("/")
def root():
    return {"service": settings.service_name, "environment": settings.environment}

@app.get("/health")
def health():
    return {"status":"healthy","service":settings.service_name}

@app.get("/ready")
def ready():
    disk = shutil.disk_usage("/")
    free_pct = round(disk.free/disk.total*100, 2)
    return {"status":"ready" if free_pct >= 5 else "degraded",
            "hostname":platform.node(),"platform":platform.system(),
            "python_version":platform.python_version(),"free_disk_percent":free_pct}

@app.post("/events", status_code=201)
def create_event(payload: EventRequest):
    with LOCK:
        try:
            event = build_event(len(EVENTS)+1, payload.severity, payload.component,
                                payload.latency_ms, payload.success)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc))
        EVENTS.append(event)
    logger.info("event_created id=%s component=%s", event.event_id, event.component)
    return event.to_dict()

@app.get("/events")
def list_events():
    with LOCK:
        return [e.to_dict() for e in EVENTS]

@app.get("/metrics")
def metrics():
    with LOCK:
        return calculate_metrics(EVENTS)

@app.delete("/events", status_code=204)
def clear_events():
    with LOCK:
        EVENTS.clear()
