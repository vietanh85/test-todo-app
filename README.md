# SORA (Smart Office Routine Assistant)

SORA is a comprehensive application designed to help office workers manage their daily routines, protect focus time, and reduce cognitive load. It features a robust FastAPI backend and a modern React frontend.

## Project Structure

- `app.py`, `main.py`, `models.py`, `database.py`: Backend (FastAPI) implementation.
- `frontend/`: Frontend (React + Vite + TypeScript) implementation.
- `docs/`: System documentation, including SRS, workflows, and technical specifications.

## Features

- **Morning Briefing**: Consolidated view of calendar, weather, and commute.
- **Deep Work Shield**: Focus mode toggle with potential for Slack/Teams integration.
- **Lunch Orchestrator**: Team voting for lunch spots.
- **Clean Slate Wrap-up**: Guided end-of-day ritual to log wins and plan tomorrow.
- **Todo Management**: Full CRUD operations for daily tasks with persistent storage.

---

## Backend Setup (FastAPI)

The backend provides a RESTful API with SQLite persistence and Pydantic models for validation.

### Prerequisites
- Python 3.9+
- pip

### Installation
```bash
pip install -r requirements.txt
```

### Running the API
```bash
python main.py
```
The API will be available at `http://localhost:8000`.

The API will be available at `http://localhost:8000`

## Authentication

This API uses Single Sign-On (SSO) via OpenID Connect (OIDC). All protected endpoints require an `Authorization: Bearer <JWT>` header.

### Configuration

Copy `.env.example` to `.env` and configure your OIDC provider:

```env
OIDC_ISSUER=https://your-idp.com
OIDC_AUDIENCE=your-client-id
JWKS_URL=https://your-idp.com/.well-known/jwks.json
```

## API Endpoints

### Base
- `GET /` - API info
- `GET /health` - Health check

### Auth
- `GET /auth/user` - Get current authenticated user information

### Todo Operations (Authenticated)
- `GET /todos` - Get current user's todos
- `GET /todos/{id}` - Get a specific todo
- `POST /todos` - Create a new todo for current user
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

### Filtering (Authenticated)
- `GET /todos/completed` - Get current user's completed todos
- `GET /todos/active` - Get current user's active todos

## Example Usage with Authentication

### Create a todo
```bash
curl -X POST "http://localhost:8000/todos" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"title": "Learn FastAPI", "description": "Complete the tutorial"}'
```

### Installation
```bash
curl "http://localhost:8000/todos" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Running the Frontend
```bash
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"completed": true}'
```
The frontend will be available at `http://localhost:5173`.

---

## Documentation

Detailed specifications can be found in the `docs/specs` directory:
- [System Design](./docs/specs/system-design.md)
- [Frontend Architecture](./docs/specs/frontend-architecture.md)
- [API Contract](./docs/specs/api-contract.md)
- [Technical Specification](./docs/specs/technical-specification.md)
- [User Stories](./docs/specs/UserStories_SORA.md)
