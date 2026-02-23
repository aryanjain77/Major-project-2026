# Introduction
Students and recent graduates often struggle to track job applications, monitor progress, follow
up, and learn from peers in competitive markets. This project proposes a digital platform that
combines organization tools, intelligent insights, and a community space to make the job search
more structured, less stressful, and more informed, while addressing issues like missed
follow-ups, poor visibility, and isolation.

# What We Are Planning to Achieve with ApplyWise
ApplyWise aims to address gaps left by existing job search tools by offering a single, cohesive
platform that is safer, privacy-first, and free. It combines an intelligent manual-capture Chrome
extension, n8n-based email classification with real-time Telegram alerts, a user-owned Google
Sheets backend for full data control, a personalized application funnel dashboard, and a
community space for anonymized peer learning—making it a customizable, student-focused
alternative designed for competitive job markets like India.

## Running with Docker

### Prerequisites

- Docker (v20.10 or newer)
- Docker Compose (included with Docker Desktop)

### Verify your installation:

```bash
docker --version
docker compose version
```

If docker compose is unavailable, you may be using the legacy Docker Compose binary:

```bash
docker-compose --version
```

From the project root directory:

```bash
docker compose up --build
```

If you are using legacy Docker Compose:
```bash
docker-compose up --build
```

This will build and start all required services (frontend, backend, database).

### Stopping the application
```bash
docker compose down
```

Note: Docker Compose v2 (docker compose) is recommended.
Legacy docker-compose is supported but deprecated.