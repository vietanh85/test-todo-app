# API Contract: Frontend-Backend Interaction

## Base URL
Default: `http://localhost:8000`

## Endpoints utilized by Frontend

### 1. GET /todos
- **Purpose**: Fetch all todo items.
- **Response Schema**:
  ```json
  [
    {
      "id": "integer",
      "title": "string",
      "description": "string | null",
      "completed": "boolean",
      "created_at": "ISO-8601 string",
      "updated_at": "ISO-8601 string"
    }
  ]
  ```

### 2. POST /todos
- **Purpose**: Create a new todo.
- **Payload**:
  ```json
  {
    "title": "string (min 1, max 200)",
    "description": "string | null (max 500)",
    "completed": "boolean (optional, default false)"
  }
  ```
- **Success Response**: 201 Created

### 3. PUT /todos/{id}
- **Purpose**: Update an existing todo (toggle status or edit content).
- **Payload**:
  ```json
  {
    "title": "string (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)"
  }
  ```

### 4. DELETE /todos/{id}
- **Purpose**: Delete a todo.
- **Success Response**: 204 No Content

### 6. POST /api/auth/login
- **Purpose**: Authenticate user and return session token.
- **Payload**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **Success Response**: 200 OK
  ```json
  {
    "token": "JWT_TOKEN_STRING",
    "user": {
      "id": "integer",
      "email": "string"
    }
  }
  ```

### 7. POST /api/auth/logout
- **Purpose**: Invalidate current session.
- **Success Response**: 200 OK

### 8. GET /health
- **Purpose**: Verify backend availability on frontend startup.

## Security Considerations
- **CORS**: Backend must allow requests from the frontend origin (e.g., `http://localhost:5173`).
- **Validation**: Frontend must mirror backend validation (e.g., title length) to provide immediate feedback.
