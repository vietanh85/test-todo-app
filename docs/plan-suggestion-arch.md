# Project Plan: SORA Architecture Implementation

## 1. Project Overview
This plan outlines the implementation of architectural improvements for the SORA (Smart Office Routine Assistant) project, as proposed in `docs/suggestion-arch.md` and reviewed in `docs/review-suggestion-arch.md`.

**Decision:** APPROVED to proceed with implementation, incorporating the senior reviewer's recommendations.

## 2. Sprint Schedule (Scrum approach)

### Sprint 1: Foundation & Refactoring (Duration: 2 weeks)
*   **Goal:** Restructure the backend and implement API versioning.
*   **Tasks:**
    *   Refactor `app.py` into a modular `APIRouter` structure (Section 6.2).
    *   Implement `/api/v1` prefix for all current and future endpoints.
    *   Integrate **Alembic** for database migrations (Review Recommendation ID 004).
    *   Implement basic **Structured Logging** (JSON) (Section 6.5).

### Sprint 2: Data & Performance (Duration: 2 weeks)
*   **Goal:** Transition to production-ready database and implement caching/background tasks.
*   **Tasks:**
    *   Setup PostgreSQL connection configuration (Section 6.1).
    *   Implement **FastAPI Background Tasks** for initial async operations (Review Recommendation ID 002).
    *   Setup Redis for caching external API results (Section 6.3).
    *   Implement application-level "Trust-but-Verify" checks for the no-auth transition (Review Recommendation ID 001).

### Sprint 3: SORA Core Features & Real-time (Duration: 2 weeks)
*   **Goal:** Implement core SORA logic and notification system.
*   **Tasks:**
    *   Develop `/briefing` and `/focus` service layer logic.
    *   Implement **Server-Sent Events (SSE)** for one-way notifications (Review Recommendation ID 003).
    *   Update Frontend to consume v1 APIs and SSE notifications.

## 3. Risk Register

| Risk ID | Description | Impact | Probability | Mitigation Strategy |
|:--- |:--- |:--- |:--- |:--- |
| R-001 | Exposure of data due to "no-auth" model | High | Medium | Implement IP allow-listing and application-level verification checks. |
| R-002 | Breaking changes during refactoring | Medium | High | Maintain high test coverage; use parallel routing during transition if necessary. |
| R-003 | External API latency/failure | Medium | Medium | Use caching (Redis) and implement robust retry logic with circuit breakers. |
| R-004 | Migration to PostgreSQL complexity | Low | Medium | Use Alembic for controlled schema migrations and test thoroughly against a staging DB. |

## 4. RACI Matrix

| Task | Project Manager | Architect | Backend Dev | Frontend Dev | DevOps |
|:--- |:---:|:---:|:---:|:---:|:---:|
| Backend Refactoring | I | A/C | R | - | - |
| API Versioning | I | C | R | C | - |
| DB Migration (PostgreSQL) | I | C | R | - | A |
| SORA Core Logic | I | C | R | - | - |
| SSE Implementation | I | C | R | R | - |
| Security Verification | A | R | R | - | C |

*R: Responsible, A: Accountable, C: Consulted, I: Informed*

## 5. Stakeholder Communication Plan
*   **Weekly Status Report:** Every Friday to all stakeholders via email.
*   **Daily Stand-up:** 15-minute sync with the dev team.
*   **Sprint Review:** End of each sprint to demo progress.
*   **Architecture Sync:** Bi-weekly meeting with the Architect to review implementation against design docs.
