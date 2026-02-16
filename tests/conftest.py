import pytest
import asyncio
import pytest_asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

import os

# Set environment variables for testing
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test_todos.db"
os.environ["OIDC_ISSUER"] = "https://test-issuer.com"
os.environ["OIDC_AUDIENCE"] = "test-audience"

from database import Base, db
from app import app
from auth import get_current_user
from models import AuthUser

# Test user data
TEST_USER = AuthUser(
    id="test-user-id",
    email="test@example.com",
    name="Test User",
    picture="https://example.com/test.png"
)

async def override_get_current_user():
    return TEST_USER

@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    async with db.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Clean up the test database file
    if os.path.exists("./test_todos.db"):
        os.remove("./test_todos.db")

@pytest_asyncio.fixture(autouse=True)
async def clear_db():
    yield
    # No need to clear separately if we recreate the DB every test,
    # but recreate_all/drop_all every test might be slow.
    # Given the current setup_test_db is function scoped now, it WILL recreate every test.


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[get_current_user] = override_get_current_user
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
