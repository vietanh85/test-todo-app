# SSO API Contract Changes

## 1. Authentication Header
All protected endpoints require an `Authorization` header with a Bearer token.

```http
Authorization: Bearer <JWT_ACCESS_TOKEN>
```

### Error Responses
- **401 Unauthorized**: Missing or invalid token.
- **403 Forbidden**: Token valid but user lacks permission (not applicable for this app's current scope).

## 2. Updated Endpoints

### 2.1 GET `/todos`
Retrieves todos belonging ONLY to the authenticated user.

- **Request**: No changes to query parameters.
- **Backend Logic**: `SELECT * FROM todos WHERE user_id = :current_user_id`.

### 2.2 POST `/todos`
Creates a new todo for the authenticated user.

- **Request Body**: Same as before.
- **Backend Logic**: Automatically assigns `user_id` from the JWT sub claim.

### 2.3 GET/PUT/DELETE `/todos/{todo_id}`
Ensures the todo belongs to the authenticated user before performing the action.

- **Backend Logic**: `SELECT * FROM todos WHERE id = :id AND user_id = :current_user_id`. If not found, return 404 (to avoid leaking existence).

## 3. New Endpoints

### 3.1 GET `/auth/user`
Retrieves information about the currently logged-in user.

- **Response Body**:
```json
{
  "id": "google-oauth2|123456789",
  "email": "user@example.com",
  "name": "John Doe",
  "picture": "https://..."
}
```

## 4. Public Endpoints
The following endpoints remain accessible without a token:
- `GET /`
- `GET /health`
- `GET /docs` (Swagger UI)
- `GET /redoc`
