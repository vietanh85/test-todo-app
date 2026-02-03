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

## API Endpoints

### Base
- `GET /` - API info

### Todo Operations
- `GET /todos` - Get all todos
- `GET /todos/{id}` - Get a specific todo
- `POST /todos` - Create a new todo
- `PUT /todos/{id}` - Update a todo
- `DELETE /todos/{id}` - Delete a todo

### Filtering
- `GET /todos/completed` - Get completed todos
- `GET /todos/active` - Get active todos

## Example Usage

### Create a todo
```bash
curl -X POST "http://localhost:8000/todos" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Complete the tutorial"}'
```

### Get all todos
```bash
curl "http://localhost:8000/todos"
```

### Update a todo
```bash
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

## API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation (Swagger UI).

Visit `http://localhost:8000/redoc` for ReDoc documentation.