# API Contract: SORA Frontend-Backend Interaction

## Base URL
Default: `http://localhost:8000/api/v1`

## Endpoints

### 1. Briefing (FR-001)
#### GET /briefing
- **Purpose**: Get the morning briefing data.
- **Response**:
  ```json
  {
    "date": "2023-10-27",
    "weather": {
      "temp": 18,
      "condition": "Cloudy",
      "advice": "Light jacket recommended."
    },
    "commute": {
      "estimated_time_mins": 45,
      "status": "Heavier than usual traffic on I-95."
    },
    "first_meeting": {
      "time": "09:30 AM",
      "title": "Project Sync"
    }
  }
  ```

### 2. Focus Mode (FR-002)
#### POST /focus/start
- **Payload**: `{"duration_mins": 90}`
#### POST /focus/stop
- **Payload**: `{}`
#### GET /focus/status
- **Response**: `{"active": true, "remaining_mins": 42}`

### 3. Lunch Group (FR-003)
#### GET /lunch/options
#### POST /lunch/vote
- **Payload**: `{"option_id": "uuid"}`

### 4. Clean Slate (FR-004)
#### GET /tasks/suggestions
- **Purpose**: Get suggested tasks for tomorrow.
#### POST /wrap-up/log
- **Payload**:
  ```json
  {
    "achievements": ["Completed API contract", "Fixed bug in auth"],
    "next_day_priorities": ["id1", "id2", "id3"]
  }
  ```

## WebSocket Events
Frontend listens on `ws://localhost:8000/ws`:
- `BRIEFING_READY`: Trigger a fetch of `/briefing`.
- `FOCUS_SUGGESTION`: Suggest entering focus mode.
- `LUNCH_POLL_STARTED`: Show lunch voting UI.

## Legacy Endpoints (Todos)
The `/todos` endpoints are maintained for individual task management within the "Clean Slate" and "Daily Log" features.

