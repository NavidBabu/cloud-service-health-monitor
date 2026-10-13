from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass(frozen=True)
class Event:
    event_id: int
    severity: str
    component: str
    latency_ms: float
    success: bool
    timestamp: str

    def to_dict(self):
        return asdict(self)

def build_event(event_id, severity, component, latency_ms, success):
    severity = severity.lower().strip()
    if severity not in {"info", "warning", "critical"}:
        raise ValueError("severity must be info, warning, or critical")
    if latency_ms < 0:
        raise ValueError("latency_ms cannot be negative")
    if not component.strip():
        raise ValueError("component is required")
    return Event(
        event_id, severity, component.strip(), round(float(latency_ms), 2),
        bool(success), datetime.now(timezone.utc).isoformat()
    )

def calculate_metrics(events):
    items = list(events)
    if not items:
        return {"event_count":0,"success_rate":1.0,"avg_latency_ms":0.0,
                "critical_events":0,"warning_events":0,"components":{}}
    components = {}
    for e in items:
        components[e.component] = components.get(e.component, 0) + 1
    return {
        "event_count": len(items),
        "success_rate": round(sum(e.success for e in items)/len(items), 4),
        "avg_latency_ms": round(sum(e.latency_ms for e in items)/len(items), 2),
        "critical_events": sum(e.severity=="critical" for e in items),
        "warning_events": sum(e.severity=="warning" for e in items),
        "components": dict(sorted(components.items()))
    }
