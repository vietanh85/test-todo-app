# Technical Specification: SSO Removal

## Overview
This document outlines the technical changes required to remove Single Sign-On (SSO) from the Todo Application.

## 1. Backend Changes (Python/FastAPI)

### 1.1. Dependency Removal
The following endpoints in `app.py` must have their `Depends(get_current_user)` removed:
- `GET /auth/user`
- `GET /todos`
- `GET /todos/completed`
- `GET /todos/active`
- `GET /todos/{todo_id}`
- `POST /todos`
- `PUT /todos/{todo_id}`
- `DELETE /todos/{todo_id}`

### 1.2. Mock User Implementation
To maintain compatibility with the existing database schema (which requires a `user_id`), a mock `current_user` should be used.

Example modification in `app.py`:
```python
DEFAULT_USER_ID = "anonymous-user"

async def get_mock_user():
    return AuthUser(
        id=DEFAULT_USER_ID,
        email="user@example.com",
        name="Default User",
        picture=None
    )
```

Replace `Depends(get_current_user)` with `Depends(get_mock_user)` where user identity is still required for database queries.

### 1.3. Clean up `auth.py`
Once the dependencies are removed, `auth.py` can be simplified or deleted. The `TokenValidator` and OIDC discovery logic are no longer needed.

## 2. Frontend Changes (React/TypeScript)

### 2.1. API Client Updates
In `frontend/src/lib/api.ts`, ensure no Authorization headers are being injected (currently they are not, so no change needed there).

### 2.2. User State Management
If the frontend used any OIDC context providers (e.g., `AuthProvider` from `react-oidc-context`), they should be removed from `main.tsx` and `App.tsx`.

### 2.3. Protected Routes
Any conditional rendering based on `isAuthenticated` should be removed to allow immediate access to the Todo list.

## 3. Database Migration
No structural changes are strictly required if we continue to use a default `user_id`. If we wish to remove the `users` table and the `user_id` foreign key:
1.  Drop the foreign key constraint on `todos.user_id`.
2.  Make `todos.user_id` nullable or remove it entirely.
3.  Drop the `users` table.

For this initial phase, we recommend keeping the schema but hardcoding the `user_id`.

## 4. Environment Variables
The following variables can be removed from `.env`:
- `OIDC_ISSUER`
- `OIDC_AUDIENCE`
- `JWKS_URL`
