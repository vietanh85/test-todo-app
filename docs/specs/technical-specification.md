# Technical Specification: SORA Frontend

## 1. Overview
This document outlines the technical implementation for the SORA (Smart Office Routine Assistant) frontend.

## 2. Core Feature Modules

### 2.1 Morning Briefing (FR-001)
- **View**: Dashboard card appearing at scheduled briefing time.
- **Components**: `BriefingCard`, `WeatherWidget`, `CommuteStatus`.
- **Data**: Aggregated from `/api/v1/briefing`.

### 2.2 Deep Work Shield (FR-002)
- **View**: Persistent "Focus Status" indicator in the header.
- **Components**: `FocusToggle`, `SessionTimer`.
- **Logic**: Polls calendar gaps or receives WebSocket event to suggest Focus Mode.

### 2.3 Lunch Orchestrator (FR-003)
- **View**: Modal or dedicated page for voting.
- **Components**: `VoteOption`, `PollResults`, `GroupSelection`.
- **Logic**: Real-time updates via WebSockets when team members vote.

### 2.4 Clean Slate Wrap-up (FR-004)
- **View**: Full-screen guided wizard at 4:45 PM.
- **Steps**:
    1. Achievement Log (Text input).
    2. Task Prioritization (Drag-and-drop list).
    3. Ritual Completion (Confetti/Success animation).

## 3. Component Hierarchy (Revised)
- `App`: Providers & Global Styles.
- `Layout`: 
    - `SideNav`: Quick access to Daily Log, Focus Settings, Team Lunch.
    - `TopBar`: Focus Mode Status, Notifications, Profile.
- `MainContent`:
    - `Dashboard`: Widgets for Briefing, active Focus session, and upcoming meetings.
    - `RitualWizard`: Multi-step container for Morning/Evening rituals.

## 4. State Management
### 4.1 Server State (React Query)
- `useBriefing()`: Daily summary data.
- `useCalendarEvents()`: Fetching upcoming meetings.
- `useTasks()`: Replacement for the old `useTodos`, integrated with Jira/Linear metadata.

### 4.2 Local State (Zustand)
- `useFocusStore`: Tracks if user is currently in Focus Mode.
- `useNotificationStore`: Manages in-app alert queue.

## 5. Integrations & Authentication
- **Auth**: OAuth2 for Google/Microsoft (handled by backend, frontend stores token).
- **Webhooks**: Frontend listens for Slack status change confirmations.

## 6. Responsive Design
- **Desktop**: Primary interface with sidebar.
- **Mobile**: Simplified list view with floating action button for quick achievement logging.
