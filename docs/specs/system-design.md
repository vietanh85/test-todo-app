# System Design: Todo Application

## Architecture Diagram (Logical)

```text
[ Browser ] <---> [ React Frontend ] <---HTTP/JSON---> [ FastAPI Backend ] <---> [ SQLite DB ]
      ^                  |                                     ^
      |                  |                                     |
      +--- User Input ---+                                     +--- SQL Queries ---+
```

## Data Flow Diagram

1. **Authentication**:
   - User submits credentials via `LoginForm`.
   - Frontend sends `POST /api/auth/login`.
   - Backend validates credentials and returns a JWT.
   - Frontend stores JWT and updates `AuthContext`.

2. **Initialization**:
   - Browser loads React application.
   - `AuthProvider` checks for existing token in storage.
   - If authenticated, `useTodos` hook triggers `GET /todos` with `Authorization` header.
   - Backend verifies JWT, extracts user ID, and queries SQLite for user-specific todos.
   - React renders the list.

3. **Creating a Todo**:
   - User types in `AddTodoForm` and submits.
   - Frontend validates input via Zod.
   - `useCreateTodo` mutation sends `POST /todos` with user's JWT.
   - Backend persists to DB (linked to user ID) and returns the new object.
   - Frontend cache is invalidated; list re-fetches.

4. **Updating a Todo**:
   - User clicks checkbox on `TodoItem`.
   - `PUT /todos/{id}` sent with `completed: !current_status` and JWT.
   - Backend verifies ownership of the todo and updates DB.

## Component Interconnection

```text
App
 └── AuthProvider (Manages JWT and User State)
      └── QueryClientProvider
           └── Layout
                ├── Header (Login/Logout buttons)
                └── Dashboard (Protected Content)
                     ├── Stats
                     ├── AddTodoForm
                     └── TodoList
                          └── TodoItem
```

## Deployment Strategy
- **Frontend**: Built as static files (SPA) and served via Nginx or hosted on Vercel/Netlify.
- **Backend**: Containerized with Docker, running Uvicorn.
- **Database**: SQLite file persisted via volume mount.
