# Backend Technical Specification: SORA

## 1. Overview
The SORA backend is a Python-based FastAPI service that acts as the orchestration layer for the Smart Office Routine Assistant. It manages integrations with external services (Calendar, Slack, Weather) and provides the core logic for productivity rituals.

## 2. Technology Stack
- **Framework:** FastAPI (Asynchronous Python).
- **ORM:** SQLAlchemy (Async).
- **Database:** SQLite (Dev) / PostgreSQL (Prod).
- **Task Queue:** Celery with Redis (for asynchronous briefing generation).
- **Authentication:** (Planned) OAuth2 with JWT validation. Currently hardcoded to `anonymous-user` per SSO removal policy.
- **Communication:** REST API for CRUD; WebSockets for real-time notifications.

## 3. Core Modules

### 3.1 Briefing Engine (`briefing_service.py`)
- **Responsibility:** Aggregates morning data.
- **Data Sources:** 
    - Google/Outlook Calendar (Meetings).
    - OpenWeatherMap (Weather).
    - Google Maps/Waze (Commute).
- **Output:** A unified JSON object delivered via `/api/v1/briefing`.

### 3.2 Focus Manager (`focus_service.py`)
- **Responsibility:** Manages "Focus Mode" lifecycle.
- **Logic:**
    - Detects calendar gaps > 90 mins.
    - Triggers Slack status updates via Webhooks.
    - Manages timer persistence.

### 3.3 Ritual Orchestrator (`ritual_service.py`)
- **Responsibility:** Handles Evening Wrap-up and Morning Planning.
- **Logic:**
    - Processes user-logged "Wins".
    - Uses a simple priority algorithm to suggest "Top 3" tasks from the `todos` table.

## 4. API Design Principles
- **Idempotency:** All POST/PUT operations should be idempotent where possible.
- **Pagination:** Large sets (e.g., historical wins) must support limit/offset or cursor-based pagination.
- **Versioning:** URL-based versioning (`/api/v1/...`).

## 5. External Integrations
- **Slack:** Uses `chat:write` and `users.profile:write` scopes.
- **Calendar:** Read-only access to `primary` calendar metadata.
- **Retry Strategy:** Exponential backoff for all external HTTP calls.

## 6. Error Handling
- **Structured Errors:** All errors returned as `{"error": "CODE", "detail": "Human-readable message"}`.
- **Logging:** Correlation IDs across services to track requests through the aggregation pipeline.
