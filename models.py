from typing import Optional
from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class User(BaseModel):
    """Model for user response"""
    id: str = Field(..., description="Unique identifier from IdP")
    email: str = Field(..., description="User's email address")
    name: Optional[str] = Field(None, description="User's full name")
    picture: Optional[str] = Field(None, description="URL to user's profile picture")

    model_config = {"from_attributes": True}


class TodoBase(BaseModel):
    """Base model for Todo with common fields"""
    title: str = Field(..., min_length=1, max_length=200, description="Title of the todo item")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")
    completed: bool = Field(False, description="Completion status")
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()


class TodoCreate(TodoBase):
    """Model for creating a new todo"""
    pass


class TodoUpdate(BaseModel):
    """Model for updating an existing todo"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Updated title")
    description: Optional[str] = Field(None, max_length=500, description="Updated description")
    completed: Optional[bool] = Field(None, description="Updated completion status")
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_empty_if_provided(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Title cannot be empty')
        return v.strip() if v else v


class Todo(TodoBase):
    """Model for todo response with database fields"""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {"from_attributes": True}
