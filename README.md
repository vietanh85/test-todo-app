# Simple Todo API

A FastAPI-based todo application with async/await support and Pydantic models.

## Installation

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

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

### Get all todos
```bash
curl "http://localhost:8000/todos" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update a todo
```bash
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{"completed": true}'
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

Visit `http://localhost:8000/redoc` for ReDoc documentation.