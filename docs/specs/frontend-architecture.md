# ADR: Frontend Architecture and Technology Stack

## Status
Proposed

## Context
The project currently has a robust FastAPI backend for managing todos. A modern, responsive, and maintainable frontend is required to provide a user interface for this system.

## Decision
We will implement the frontend using the following technology stack:

1.  **Framework**: React (v18+) with TypeScript.
    *   *Reasoning*: Large ecosystem, strong type safety, and industry standard for building interactive UIs.
2.  **Build Tool**: Vite.
    *   *Reasoning*: Extremely fast development server and optimized build process compared to Create React App.
3.  **Server State Management**: TanStack Query (React Query).
    *   *Reasoning*: Handles caching, background updates, and stale data out of the box. Perfect for RESTful APIs.
4.  **Styling**: Tailwind CSS.
    *   *Reasoning*: Utility-first approach allows for rapid UI development and consistent design without writing custom CSS files.
5.  **UI Components**: Shadcn/UI (Radix UI + Lucide Icons).
    *   *Reasoning*: Provides accessible, unstyled components that are easy to customize and look modern.
6.  **Form Management**: React Hook Form with Zod validation.
    *   *Reasoning*: Lightweight form handling that integrates perfectly with TypeScript for schema-based validation.

## Architecture
The frontend will follow a modular architecture:
*   `src/api`: API client and React Query hooks.
*   `src/components`: Reusable UI components (atomic design).
*   `src/hooks`: Custom React hooks for logic reuse.
*   `src/types`: TypeScript interfaces and types.
*   `src/lib`: Utility functions and configurations (e.g., axios instance).

## Consequences
*   **Pros**:
    *   High development velocity.
    *   Strong type safety across the application.
    *   Excellent performance and developer experience.
    *   Accessible UI components by default.
*   **Cons**:
    *   Initial setup overhead for TypeScript and Tailwind.
    *   Learning curve for TanStack Query for developers only familiar with `useEffect` fetching.
