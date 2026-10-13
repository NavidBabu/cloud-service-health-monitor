# Cloud Service Health Monitor

A cloud-native Python portfolio project demonstrating Linux-oriented development, REST APIs, testing, Docker, CI, and Kubernetes deployment concepts.

> Educational project only. All telemetry is synthetic.

## Features
- FastAPI REST service
- `/health` liveness endpoint
- `/ready` readiness endpoint
- `/events` synthetic telemetry API
- `/metrics` success-rate, latency, severity, and component metrics
- environment-based configuration
- structured logging
- Python unit tests
- Docker + Docker Compose
- Linux health-check script
- GitHub Actions CI
- Kubernetes Deployment + Service manifests

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

Open `http://127.0.0.1:8080/docs`.

## Docker
```bash
docker build -t cloud-service-health-monitor:local .
docker run --rm -p 8080:8080 cloud-service-health-monitor:local
```

## Example event
```bash
curl -X POST http://127.0.0.1:8080/events   -H "Content-Type: application/json"   -d '{"severity":"warning","component":"api-gateway","latency_ms":42.8,"success":true}'
```

## Resume bullets
**Cloud Service Health Monitor — Python, Linux, FastAPI, Docker, Kubernetes**
- Built a containerized Python/FastAPI service exposing REST endpoints for liveness, readiness, synthetic telemetry, and operational metrics in a Linux-oriented environment.
- Implemented input validation, environment-based configuration, structured logging, health probes, and unit-tested metrics logic.
- Containerized the service with Docker, added GitHub Actions CI, and created Kubernetes manifests with liveness/readiness probes and resource controls.
