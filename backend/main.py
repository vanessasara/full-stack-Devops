"""
Sony Interior - FastAPI Backend
Main application entry point with CORS configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager for startup and shutdown events
    """
    # Startup
    logger.info("Starting Sony Interior Backend API...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")

    # Initialize database connection pool
    try:
        from database import get_database_pool, test_database_connection
        await get_database_pool()

        # Test database connection
        db_connected = await test_database_connection()
        if db_connected:
            logger.info("✅ Database connection pool initialized")
        else:
            logger.warning("⚠️  Database connection test failed")
    except Exception as e:
        logger.error(f"❌ Failed to initialize database: {e}")
        logger.warning("API will start but database operations will fail")

    # Initialize embedding model
    # TODO: Add embedding model initialization in Phase 11

    yield

    # Shutdown
    logger.info("Shutting down Sony Interior Backend API...")

    # Cleanup database connections
    try:
        from database import close_database_pool
        await close_database_pool()
        logger.info("✅ Database connection pool closed")
    except Exception as e:
        logger.error(f"Error closing database pool: {e}")


# Create FastAPI application
app = FastAPI(
    title="Sony Interior Backend API",
    description="AI-powered furniture consultation backend with RAG capabilities",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = [
    "http://localhost:3000",  # Next.js development server
    "http://127.0.0.1:3000",  # Alternative localhost
    os.getenv("NEXT_PUBLIC_API_URL", "http://localhost:3000"),  # Environment-based
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Root endpoint
@app.get("/")
async def root():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "message": "Sony Interior Backend API is running",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """
    Detailed health check endpoint
    """
    # Check database connection
    db_status = "unknown"
    try:
        from database import test_database_connection
        db_connected = await test_database_connection()
        db_status = "connected" if db_connected else "disconnected"
    except Exception as e:
        db_status = f"error: {str(e)[:50]}"

    return {
        "status": "healthy",
        "database": db_status,
        "embedding_model": "not_initialized",  # Will update in Phase 11
        "mcp_servers": "not_initialized"  # Will update in Phase 12
    }


# TODO: Mount routers in later phases
# from routers import chat
# app.include_router(chat.router, prefix="/api", tags=["chat"])


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
