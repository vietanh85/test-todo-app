# Architecture Review & Suggestions Report

## 1. Executive Summary
This report provides a comprehensive review of the current SORA (Smart Office Routine Assistant) architecture. While the foundational stack is modern and well-chosen, there are significant gaps between the planned features (as per documentation) and the current implementation. This document outlines suggestions to improve scalability, maintainability, and feature parity.

---

## 2. Current Architecture Overview

### 2.1 Backend Stack
- **Framework**: FastAPI (Asynchronous Python)
- **ORM**: SQLAlchemy with `asyncio` support
- **Database**: SQLite (local file-based)
- **Authentication**: OIDC (OpenID Connect) with JWT validation and local user synchronization

### 2.2 Frontend Stack
- **Framework**: React 18+ with TypeScript
- **Build Tool**: Vite
- **State Management**: TanStack Query (Server state), Zustand (Client UI state)
- **Styling**: Tailwind CSS + Shadcn/UI

### 2.3 Deployment & Infrastructure
- **Containerization**: Docker/Podman
- **Target Platform**: AWS ECS (Fargate) for Backend, Vercel/Netlify for Frontend

---

## 3. Strengths
- **Modern Core**: Choice of FastAPI and React/Vite ensures a high-performance, developer-friendly environment.
- **Type Safety**: End-to-end type safety using Pydantic (Backend) and TypeScript (Frontend).
- **Asynchronous Foundation**: Full use of `async`/`await` for I/O operations (DB, Auth).
- **Flexibility**: The current design (SQLAlchemy + Pydantic) allows for relatively easy transitions between different authentication and database models.

---

## 4. Authentication Strategy Transition
There is currently a proposal (ADR 002) to remove the Single Sign-On (SSO) layer and move towards a "no-auth" or "single-user" model for simplicity. 

**Architectural Impact**:
- **Simplicity**: Reduced operational overhead by removing dependency on external Identity Providers (IdP).
- **Security Responsibility Shift**: In a "no-auth" model, the application itself is no longer responsible for identity. Security must be handled at the infrastructure level (e.g., VPN, VPC, or an authenticating reverse proxy like Authelia/Nginx).
- **Multi-tenancy**: The application will transition to a shared-data model unless local user management is introduced later.

---

## 5. Identified Gaps & Areas for Improvement

### 5.1 Scalability Concerns
- **Database**: SQLite is excellent for development but lacks robust support for high concurrency and horizontal scaling in a production environment like AWS Fargate.
- **Caching**: Lack of a caching layer (e.g., Redis) for frequently accessed data or external API results (Weather, Commute).

### 5.2 Code Organization
- **Monolithic API**: Currently, all endpoints and logic reside in `app.py`. As SORA features (Briefing, Focus Mode, Lunch Group) are added, this file will become unmaintainable.
- **Tight Coupling**: Database logic and API routing are heavily intertwined.

### 5.3 Feature Discrepancy
- **Missing SORA Logic**: The `api-contract.md` defines several complex features (Briefing, Focus Mode, Lunch Group, Clean Slate) that are not yet reflected in the backend implementation.
- **Real-time Notifications**: Documentation mentions WebSockets for events like `BRIEFING_READY`, but no implementation exists in the current codebase.

### 5.4 Operational Gaps
- **API Versioning**: Routes like `/todos` lack explicit URL versioning (e.g., `/api/v1/todos`).
- **Observability**: Basic logging is present, but structured logging, request tracing, and performance monitoring (APM) are missing.

---

## 6. Architectural Suggestions

### 6.1 Database Migration (PostgreSQL)
**Suggestion**: Replace SQLite with PostgreSQL for production.
- **Reasoning**: Better support for concurrent writes, rich data types, and seamless integration with managed services like AWS RDS.
- **Action**: Update `DATABASE_URL` and ensure SQLAlchemy models remain compatible.

### 6.2 Modular Backend Structure
**Suggestion**: Refactor `app.py` into a modular structure using FastAPI's `APIRouter`.
- **Proposed Layout**:
  ```text
  app/
  ├── api/
  │   ├── v1/
  │   │   ├── endpoints/
  │   │   │   ├── todos.py
  │   │   │   ├── briefing.py
  │   │   │   ├── focus.py
  │   │   │   └── lunch.py
  │   │   └── api.py (Router aggregation)
  ├── core/ (config, security)
  ├── crud/ (DB operations)
  ├── models/ (SQLAlchemy models)
  ├── schemas/ (Pydantic models)
  └── services/ (Business logic for external integrations)
  ```

### 6.3 Asynchronous Task Processing
**Suggestion**: Introduce a task queue (e.g., **Celery** or **ARQ**) with **Redis**.
- **Reasoning**: SORA needs to fetch data from external APIs (Weather, Google Maps, Slack). These operations should be handled asynchronously to avoid blocking API responses and to support scheduled tasks (e.g., pre-fetching morning briefings).

### 6.4 Real-time Communication (WebSocket/SSE)
**Suggestion**: Implement a WebSocket manager within FastAPI.
- **Reasoning**: To support "Ritual" notifications and real-time lunch voting as described in `Workflows_SORA.md`.

### 6.5 Enhanced Observability
**Suggestion**: 
- Implement **Structured Logging** (JSON) for easier parsing in CloudWatch/ELK.
- Integrate **Sentry** or **OpenTelemetry** for error tracking and performance profiling.

### 6.6 Infrastructure Improvements
**Suggestion**: 
- **API Gateway**: Use an AWS ALB or API Gateway to handle rate limiting and SSL termination.
- **CI/CD**: Implement automated testing (pytest) and deployment pipelines to ensure code quality.

---

## 7. Implementation Roadmap (Priority Order)
1.  **Refactor Backend**: Move to a modular router-based structure.
2.  **API Versioning**: Implement `/api/v1` prefix for all endpoints.
3.  **Database Migration**: Setup PostgreSQL connection for non-local environments.
4.  **SORA Core Implementation**: Build the `/briefing` and `/focus` logic using a service-layer pattern.
5.  **Real-time Layer**: Add WebSocket support for notifications.
6.  **Caching & Tasks**: Integrate Redis for performance and background fetching.
