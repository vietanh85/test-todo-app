# System Design: Todo Application

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

## Data Flow Diagram

0. **Authentication**:
   - User logs in via IdP.
   - Frontend receives and stores Access Token.

1. **Initialization**:
   - Browser loads React application.
   - `useAuth` checks login status.
   - `useTodos` hook triggers `GET /todos` with `Authorization: Bearer <token>`.
   - Backend validates JWT, extracts `user_id`, queries SQLite for user-specific todos.
   - React renders the list.

2. **Creating a Todo**:
   - User types in `AddTodoForm` and submits.
   - Frontend validates input via Zod.
   - `useCreateTodo` mutation sends `POST /todos`.
   - Backend persists to DB and returns the new object.
   - Frontend cache is invalidated; list re-fetches.

3. **Updating a Todo**:
   - User clicks checkbox on `TodoItem`.
   - Frontend optimistic update (optional) or immediate mutation.
   - `PUT /todos/{id}` sent with `completed: !current_status`.
   - Backend updates DB and returns updated object.

## Component Interconnection

```text
App
 └── QueryClientProvider
      └── Layout
           ├── Header
           └── Dashboard
                ├── Stats (Aggregates data from useTodos)
                ├── AddTodoForm (Uses useCreateTodo)
                └── TodoList
                     └── TodoItem (Uses useUpdateTodo, useDeleteTodo)
```

## Deployment Strategy
- **Frontend**: Built as static files (SPA) and served via Nginx or hosted on Vercel/Netlify.
- **Backend**: Containerized with Docker, running Uvicorn.
- **Database**: SQLite file persisted via volume mount.
