## Introduction
Students and recent graduates often struggle to track job applications, monitor progress, follow
up, and learn from peers in competitive markets. This project proposes a digital platform that
combines organization tools, intelligent insights, and a community space to make the job search
more structured, less stressful, and more informed, while addressing issues like missed
follow-ups, poor visibility, and isolation.

## What We Are Planning to Achieve with ApplyWise
ApplyWise aims to address gaps left by existing job search tools by offering a single, cohesive
platform that is safer, privacy-first, and free. It combines an intelligent manual-capture Chrome
extension, n8n-based email classification with real-time Telegram alerts, a user-owned Google
Sheets backend for full data control, a personalized application funnel dashboard, and a
community space for anonymized peer learning—making it a customizable, student-focused
alternative designed for competitive job markets like India.

## Monorepo Structure
This repository is organized as a monorepo under the `applywise/` directory:

- `applywise/apps/web`: React dashboard (Vite) client.
- `applywise/apps/extension`: Chrome extension client.
- `applywise/apps/ai-service`: Python Flask AI service.
- `applywise/packages/api`: Node.js/Express backend (community + future gateway).
- `applywise/packages/shared`: Shared types and utilities (to be filled in future phases).
- `applywise/packages/ui`: Shared UI components (to be filled in future phases).
- `applywise/infrastructure/docker`: Containerization assets.
- `applywise/infrastructure/nginx`: Reverse proxy configuration.
- `applywise/infrastructure/n8n`: n8n workflow exports and infra.

Existing behavior is unchanged in this phase; projects have only been moved into the monorepo layout to prepare for incremental refactoring.
