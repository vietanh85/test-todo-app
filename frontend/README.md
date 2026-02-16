# SORA Frontend (Smart Office Routine Assistant)

## Overview
This is the React-based frontend for SORA, designed to help office workers manage their daily routines, protect focus time, and reduce cognitive load.

## Tech Stack
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS + Shadcn/UI
- **State Management**: 
  - Server: TanStack Query (React Query)
  - Client: Zustand
- **Forms**: React Hook Form + Zod

## Key Features
1. **Morning Briefing**: Consolidated view of calendar, weather, and commute.
2. **Deep Work Shield**: Focus mode toggle with Slack/Teams integration.
3. **Lunch Orchestrator**: Team voting for lunch spots.
4. **Clean Slate Wrap-up**: Guided end-of-day ritual to log wins and plan tomorrow.

## Getting Started
1. Install dependencies:
   ```bash
   npm install
   ```
2. Set up environment variables:
   - Create a `.env` file based on `.env.example`.
3. Run the development server:
   ```bash
   npm run dev
   ```

## Architecture
See detailed documentation in `/docs/specs/`:
- [Frontend Architecture](../docs/specs/frontend-architecture.md)
- [Technical Specification](../docs/specs/technical-specification.md)
- [API Contract](../docs/specs/api-contract.md)
