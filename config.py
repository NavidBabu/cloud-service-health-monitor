import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    service_name: str = os.getenv("SERVICE_NAME", "cloud-service-health-monitor")
    environment: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    max_events: int = int(os.getenv("MAX_EVENTS", "500"))

settings = Settings()
