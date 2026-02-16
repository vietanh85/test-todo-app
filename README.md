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

### API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Frontend Setup (React)

The frontend is built with React, Vite, and Tailwind CSS, using TanStack Query for state management.

### Prerequisites
- Node.js (v18+)
- npm

### Installation
```bash
cd frontend
npm install
```

### Running the Frontend
```bash
npm run dev
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
