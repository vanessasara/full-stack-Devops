"""
Database connection module for Neon Postgres with pgvector support
"""

import asyncpg
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_database_pool() -> asyncpg.Pool:
    """
    Get or create database connection pool
    """
    global _pool

    if _pool is None:
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        try:
            _pool = await asyncpg.create_pool(
                database_url,
                min_size=2,
                max_size=10,
                command_timeout=60,
                timeout=30,
            )
            logger.info("Database connection pool created successfully")

        except Exception as e:
            logger.error(f"Failed to create database connection pool: {e}")
            raise

    return _pool


async def close_database_pool():
    """
    Close database connection pool
    """
    global _pool

    if _pool is not None:
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


async def get_db():
    """
    Dependency injection function for database connection
    Use this in FastAPI route dependencies
    """
    pool = await get_database_pool()
    async with pool.acquire() as connection:
        yield connection


async def enable_pgvector_extension():
    """
    Enable pgvector extension in the database
    Run this once during initial setup
    """
    pool = await get_database_pool()

    async with pool.acquire() as connection:
        try:
            await connection.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            logger.info("pgvector extension enabled successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to enable pgvector extension: {e}")
            raise


async def test_database_connection() -> bool:
    """
    Test database connection
    Returns True if connection is successful
    """
    try:
        pool = await get_database_pool()

        async with pool.acquire() as connection:
            result = await connection.fetchval("SELECT 1")

            if result == 1:
                logger.info("Database connection test successful")
                return True
            else:
                logger.error("Database connection test failed")
                return False

    except Exception as e:
        logger.error(f"Database connection test error: {e}")
        return False


async def get_database_version() -> str:
    """
    Get PostgreSQL version information
    """
    pool = await get_database_pool()

    async with pool.acquire() as connection:
        version = await connection.fetchval("SELECT version()")
        return version
