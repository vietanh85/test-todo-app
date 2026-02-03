import os
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./todos.db")
DB_ECHO = os.getenv("DB_ECHO", "false").lower() in ("true", "1", "t")

Base = declarative_base()


class TodoDB(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class Database:
    def __init__(self):
        self.engine = create_async_engine(DATABASE_URL, echo=DB_ECHO)
        self.async_session = async_sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    async def create_tables(self):
        """Create database tables"""
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Failed to create database tables: {e}")
            raise
    
    async def dispose(self):
        """Dispose of the database engine"""
        try:
            await self.engine.dispose()
            logger.info("Database engine disposed successfully")
        except Exception as e:
            logger.error(f"Failed to dispose database engine: {e}")
            raise
    
    def session(self) -> AsyncSession:
        """Get async database session for use as async context manager"""
        return self.async_session()


# Global database instance
db = Database()
