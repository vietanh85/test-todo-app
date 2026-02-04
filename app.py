from typing import List, Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from datetime import datetime
from sqlalchemy import select, delete, insert
from sqlalchemy.exc import SQLAlchemyError
from models import Todo, TodoCreate, TodoUpdate, User, UserCreate, Token, LoginRequest, TokenData
from database import db, TodoDB, UserDB
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
        
    async with db.session() as session:
        result = await session.execute(select(UserDB).where(UserDB.email == token_data.email))
        user = result.scalar_one_or_none()
        if user is None:
            raise credentials_exception
        return user


@app.get("/", response_model=dict)
async def root():
    """Get API information"""
    return {
        "message": "Simple Todo API", 
        "version": "1.0.0",
        "status": "operational"
    }


@app.post("/api/auth/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate):
    """Register a new user"""
    try:
        async with db.session() as session:
            # Check if user already exists
            result = await session.execute(select(UserDB).where(UserDB.email == user_in.email))
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            
            new_user = UserDB(
                email=user_in.email,
                hashed_password=get_password_hash(user_in.password)
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return User.model_validate(new_user)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in register: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@app.post("/api/auth/login", response_model=Token)
async def login(login_data: LoginRequest):
    """Login and get access token"""
    try:
        async with db.session() as session:
            result = await session.execute(select(UserDB).where(UserDB.email == login_data.email))
            user = result.scalar_one_or_none()
            
            if not user or not verify_password(login_data.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            access_token = create_access_token(data={"sub": user.email})
            return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@app.post("/api/auth/logout")
async def logout():
    """Logout endpoint (client side usually handles this by discarding token)"""
    return {"message": "Successfully logged out"}


@app.get("/todos", response_model=List[Todo])
async def get_todos(current_user: UserDB = Depends(get_current_user)):
    """Get all todos for the current user"""
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB)
                .where(TodoDB.user_id == current_user.id)
                .order_by(TodoDB.created_at.desc())
            )
            todos = result.scalars().all()
            return [Todo.model_validate(todo) for todo in todos]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve todos"
        )


@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, current_user: UserDB = Depends(get_current_user)):
    """Get a specific todo by ID for current user"""
    validate_todo_id(todo_id)
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB)
                .where(TodoDB.id == todo_id)
                .where(TodoDB.user_id == current_user.id)
            )
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


@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate, current_user: UserDB = Depends(get_current_user)):
    """Create a new todo for the current user"""
    try:
        current_time = datetime.now()
        
        new_todo = TodoDB(
            title=todo.title,
            description=todo.description,
            completed=todo.completed,
            user_id=current_user.id,
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


@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate, current_user: UserDB = Depends(get_current_user)):
    """Update an existing todo for current user"""
    validate_todo_id(todo_id)
    try:
        async with db.session() as session:
            # Get existing todo with row lock to prevent race conditions
            result = await session.execute(
                select(TodoDB)
                .where(TodoDB.id == todo_id)
                .where(TodoDB.user_id == current_user.id)
                .with_for_update()
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
async def delete_todo(todo_id: int, current_user: UserDB = Depends(get_current_user)):
    """Delete a todo for current user"""
    validate_todo_id(todo_id)
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB)
                .where(TodoDB.id == todo_id)
                .where(TodoDB.user_id == current_user.id)
                .with_for_update()
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


@app.get("/todos/completed", response_model=List[Todo])
async def get_completed_todos(current_user: UserDB = Depends(get_current_user)):
    """Get all completed todos for current user"""
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB)
                .where(TodoDB.completed == True)
                .where(TodoDB.user_id == current_user.id)
                .order_by(TodoDB.updated_at.desc())
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
async def get_active_todos(current_user: UserDB = Depends(get_current_user)):
    """Get all active (incomplete) todos for current user"""
    try:
        async with db.session() as session:
            result = await session.execute(
                select(TodoDB)
                .where(TodoDB.completed == False)
                .where(TodoDB.user_id == current_user.id)
                .order_by(TodoDB.created_at.desc())
            )
            todos = result.scalars().all()
            return [Todo.model_validate(todo) for todo in todos]
    except SQLAlchemyError as e:
        logger.error(f"Database error in get_active_todos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve active todos"
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
