# OpenTelemetry Tracing Demo

Next.js + Django + MySQL with OpenTelemetry automatic instrumentation.

## Architecture

- **Frontend**: Next.js (App Router) on `http://localhost:3000`
- **Backend**: Django REST API on `http://localhost:8000`
- **Database**: MySQL on `localhost:3306`
- **Telemetry**: OpenTelemetry Collector on ports 4317 (gRPC) and 4318 (HTTP)

## Data Flow

1. User accesses `http://localhost:3000/`
2. Next.js fetches data from `http://backend:8000/api/users`
3. Django queries MySQL for user data (100 sample records)
4. All traces are sent to OpenTelemetry Collector and output to console via debug exporter

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Run the Application

```bash
docker compose up --build
```

### Access the Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/users
- MySQL: localhost:3306 (user: dbuser, password: dbpassword, database: userdb)

### View Traces

Traces will be displayed in the OpenTelemetry Collector console output. Look for the `otel-collector` container logs:

```bash
docker compose logs -f otel-collector
```

### Stop the Application

```bash
docker compose down
```

To remove volumes as well:

```bash
docker compose down -v
```

## Project Structure

```
.
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.js
│   ├── instrumentation.ts          # OpenTelemetry setup
│   └── app/
│       ├── layout.tsx
│       └── page.tsx                # Main page that calls backend API
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py             # Django settings with MySQL config
│   │   └── urls.py                 # URL routing
│   └── users/
│       ├── models.py                # User model
│       └── views.py                 # API endpoint
├── mysql/
│   └── init.sql                     # Initial data (100 users)
└── otel-collector/
    └── config.yaml                  # OTEL Collector config with debug exporter
```

## OpenTelemetry Configuration

### Next.js (Node.js)
- Auto-instrumentation via `@opentelemetry/auto-instrumentations-node`
- OTLP gRPC exporter to Collector
- Configured in `instrumentation.ts`

### Django (Python)
- Auto-instrumentation via `opentelemetry-instrument` CLI
- Includes Django and MySQL instrumentation
- OTLP exporter to Collector

### Collector
- Receives traces via OTLP (gRPC and HTTP)
- Exports to console via debug exporter
- Configuration in `otel-collector/config.yaml`
