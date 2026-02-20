# Non-SSO API Contract

## 1. Authentication
Authentication is no longer required for any API endpoints. The `Authorization` header is ignored if provided.

## 2. Endpoints

### 2.1 GET `/todos`
Retrieves all todos from the shared pool (or associated with the default 'anonymous-user').

- **Request**: No headers or query parameters required for identity.
- **Backend Logic**: `SELECT * FROM todos WHERE user_id = 'anonymous-user'`.

### 2.2 POST `/todos`
Creates a new todo.

- **Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false
}
```
- **Backend Logic**: Automatically assigns `user_id = 'anonymous-user'`.

### 2.3 GET/PUT/DELETE `/todos/{todo_id}`
Performs actions on a specific todo.

- **Backend Logic**: `SELECT * FROM todos WHERE id = :id`. Access is granted to all todos.

### 2.4 GET `/auth/user`
This endpoint is deprecated but remains for backward compatibility. It returns a hardcoded mock user.

- **Response Body**:
```json
{
  "id": "anonymous-user",
  "email": "user@example.com",
  "name": "Default User",
  "picture": null
}
```

## 3. Public Endpoints
All endpoints are now public:
- `GET /`
- `GET /health`
- `GET /todos`
- `POST /todos`
- `GET /todos/{todo_id}`
- `PUT /todos/{todo_id}`
- `DELETE /todos/{todo_id}`
- `GET /docs`
