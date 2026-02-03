from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from datetime import datetime
from models import Todo, TodoCreate, TodoUpdate


app = FastAPI(title="Simple Todo API", version="1.0.0")

todos_db = {}
next_id = 1


@app.get("/", response_model=dict)
async def root():
    return {"message": "Simple Todo API", "version": "1.0.0"}


@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return list(todos_db.values())


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todos_db[todo_id]


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    global next_id
    current_time = datetime.now()
    
    new_todo = Todo(
        id=next_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=current_time,
        updated_at=current_time
    )
    
    todos_db[next_id] = new_todo
    next_id += 1
    
    return new_todo


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    stored_todo = todos_db[todo_id]
    update_data = todo_update.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(stored_todo, field, value)
    
    stored_todo.updated_at = datetime.now()
    
    return stored_todo


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    if todo_id not in todos_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    del todos_db[todo_id]


@app.get("/todos/completed", response_model=List[Todo])
async def get_completed_todos():
    return [todo for todo in todos_db.values() if todo.completed]


@app.get("/todos/active", response_model=List[Todo])
async def get_active_todos():
    return [todo for todo in todos_db.values() if not todo.completed]