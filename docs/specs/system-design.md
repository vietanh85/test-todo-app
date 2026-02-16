# System Design: SORA (Smart Office Routine Assistant)

## Architecture Diagram (Logical)

```text
[ Browser ] <---> [ React Frontend ] <---HTTP/JSON---> [ FastAPI Backend ] <---> [ SQLite DB ]
      ^                  |      ^                              ^
      |                  |      |                              |
      +--- User Input ---+      +--- Bearer Token (JWT) -------+
                                |
                        [ Identity Provider ]
                        (Google/GitHub/Auth0)
```

## Data Flow Diagram (SORA Rituals)

0. **Authentication**:
   - User logs in via IdP.
   - Frontend receives and stores Access Token.

1. **Initialization**:
   - Browser loads React application.
   - `useAuth` checks login status.
   - `useTodos` hook triggers `GET /todos` with `Authorization: Bearer <token>`.
   - Backend validates JWT, extracts `user_id`, queries SQLite for user-specific todos.
   - React renders the list.

2. **Focus Mode Workflow**:
   - Frontend `useFocusStore` monitors calendar gaps (calculated by backend).
   - User clicks "Enter Focus Mode".
   - Frontend sends POST to `/api/v1/focus/start`.
   - Backend updates Slack status via Webhook.
   - Frontend starts countdown timer.

3. **Evening Wrap-up (Clean Slate)**:
   - Frontend detects 4:45 PM or receives push.
   - Frontend switches view to `RitualWizard`.
   - User inputs achievements.
   - Backend persists "Wins" and generates "Top 3" for tomorrow.

## Component Interconnection (Frontend)

```text
App
 ├── NotificationProvider (Toast & Push)
 └── Layout
      ├── Sidebar (Nav: Home, Stats, Focus, Team)
      └── MainContent
           ├── Dashboard (Widgets: Briefing, focus-session)
           └── RitualOverlay (Modals/Wizards for Morning/Evening)
```

## Security & Privacy
- **OAuth2**: All external integrations use user-specific OAuth tokens.
- **Data Minimization**: Backend only processes calendar metadata; no sensitive body content is stored.
- **Local Storage**: Preferences and UI state stored in browser for speed.

## Deployment Strategy
- **Frontend**: Vite build hosted on Vercel/Netlify for global CDN performance.
- **Backend**: AWS ECS (Fargate) for scalable FastAPI service.
- **Real-time**: AWS AppSync or dedicated WebSocket server (Socket.io) if needed for scaling team lunch votes.
