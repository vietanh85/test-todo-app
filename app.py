from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from models import Todo, TodoCreate, TodoUpdate
from database import db, TodoDB
import logging
from contextlib import asynccontextmanager
import os
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS if o.strip()] or ["*"]


def validate_todo_id(todo_id: int) -> None:
    """Validate that todo_id is a positive integer"""
    if todo_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid todo_id: must be a positive integer"
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    try:
        await db.create_tables()
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")
    await db.dispose()


app = FastAPI(
    title="Simple Todo API", 
    version="1.0.0",
    description="A production-ready Todo API with SQLite persistence",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ORIGINS != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=dict)
async def root():
    """Get API information"""
    return {
        "message": "Simple Todo API", 
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/todos", response_model=List[Todo])
async def get_todos():
    """Get all todos"""
    try:
        async with db.session() as session:
            result = await session.execute(select(TodoDB).order_by(TodoDB.created_at.desc()))
            todos = result.scalars().all()
            return [Todo.model_validate(todo) for todo in todos]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todos"
        )


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    """Create a new todo"""
    try:
        current_time = datetime.now()
        
        new_todo = TodoDB(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            created_at=current_time
        )
        
        async with db.session() as session:
            session.add(new_todo)
            await session.commit()
            await session.refresh(new_todo)
            logger.info(f"Created todo with id: {new_todo.id}")
            
            return Todo.model_validate(new_todo)
            
    except ValueError as e:
        logger.error(f"Validation error in create_todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in create_todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create todo"
        )


# IMPORTANT: Specific paths must be defined before dynamic paths (like /{todo_id})
# to ensure correct route matching.

@app.get("/todos/completed", response_model=List[Todo])
async def get_completed_todos():
    """Get all completed todos"""
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB).where(TodoDB.completed == True).order_by(TodoDB.updated_at.desc())
            )
            todos = result.scalars().all()
            return [Todo.model_validate(todo) for todo in todos]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_completed_todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve completed todos"
        )


@app.get("/todos/active", response_model=List[Todo])
async def get_active_todos():
    """Get all active (incomplete) todos"""
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB).where(TodoDB.completed == False).order_by(TodoDB.created_at.desc())
            )
            todos = result.scalars().all()
            return [Todo.model_validate(todo) for todo in todos]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_active_todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve active todos"
        )


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    validate_todo_id(todo_id)
    try:
        async with db.session() as session:
            result = await session.execute(select(TodoDB).where(TodoDB.id == todo_id))
            todo = result.scalar_one_or_none()
            
            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo with id {todo_id} not found"
                )
            
            return Todo.model_validate(todo)
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todo"
        )


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """Update an existing todo"""
    validate_todo_id(todo_id)
    try:
        async with db.session() as session:
            # Get existing todo with row lock to prevent race conditions
            result = await session.execute(
                select(TodoDB).where(TodoDB.id == todo_id).with_for_update()
            )
            todo = result.scalar_one_or_none()
            
            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo with id {todo_id} not found"
                )
            
            for field, value in todo_update.model_dump(exclude_unset=True).items():
                setattr(todo, field, value)
            
            await session.commit()
            await session.refresh(todo)
            logger.info(f"Updated todo with id: {todo_id}")
            
            return Todo.model_validate(todo)
            
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error in update_todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error in update_todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update todo"
        )


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    """Delete a todo"""
    validate_todo_id(todo_id)
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB).where(TodoDB.id == todo_id).with_for_update()
            )
            todo = result.scalar_one_or_none()
            
            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Todo with id {todo_id} not found"
                )
            
            await session.delete(todo)
            await session.commit()
            logger.info(f"Deleted todo with id: {todo_id}")
            
            return None
            
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"Database error in delete_todo: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete todo"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint with database connection timeout"""
    try:
        async with asyncio.timeout(5.0):
            async with db.session() as session:
                result = await session.execute(select(TodoDB).limit(1))
                result.scalar_one_or_none()
        return {"status": "healthy", "database": "connected", "timestamp": datetime.now()}
    except TimeoutError:
        logger.error("Health check failed: database query timeout")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database query timeout"
        )
    except SQLAlchemyError as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )
