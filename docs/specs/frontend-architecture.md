# ADR: SORA Frontend Architecture and Technology Stack

## Status
Proposed (Revised for SORA)

## Context
The project is evolving from a simple Todo app into the Smart Office Routine Assistant (SORA). SORA requires a highly interactive, real-time frontend that can handle notifications, external integrations (Calendar, Slack), and various "rituals" (Morning Briefing, Clean Slate).

## Decision
We will implement the SORA frontend using the following technology stack:

1.  **Framework**: React (v18+) with TypeScript.
    *   *Reasoning*: Industry standard for interactive UIs with strong type safety.
2.  **Build Tool**: Vite.
    *   *Reasoning*: Fast development and optimized builds.
3.  **Server State Management**: TanStack Query (React Query).
    *   *Reasoning*: Essential for managing asynchronous data from backend and external APIs (Weather, Traffic).
4.  **Styling**: Tailwind CSS with Radix UI (via Shadcn/UI).
    *   *Reasoning*: Rapid development of accessible, modern components.
5.  **State Management (Client)**: Zustand.
    *   *Reasoning*: For global UI state that doesn't fit in React Query (e.g., notification preferences, active Focus Mode status).
6.  **Real-time / Notifications**: WebSockets or Server-Sent Events (SSE).
    *   *Reasoning*: Required for pushed notifications (Morning Briefing, Micro-break reminders).
7.  **Form Management**: React Hook Form with Zod.

## Architecture
The frontend will follow a feature-based modular architecture:
*   `src/features`: Divided by SORA functionality (e.g., `features/briefing`, `features/focus-mode`, `features/wrap-up`).
*   `src/api`: Centralized API clients and generic React Query configurations.
*   `src/components/ui`: Low-level UI components (Buttons, Inputs).
*   `src/store`: Global Zustand stores.
*   `src/hooks`: Shared logic (e.g., `useNotification`).

## Consequences
*   **Pros**:
    *   Scalable structure for complex features.
    *   Real-time capabilities integrated early.
    *   Consistent UI across different modules.
*   **Cons**:
    *   Increased complexity due to real-time requirements.
    *   Need for robust error handling for third-party integrations.
