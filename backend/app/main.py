from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import db
from app.core.redis import redis_client
from app.core.vector_db import vector_db
from app.core.errors import AppException
from app.api import router as api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting up Telugu AI Tutor...")
    try:
        await db.connect()
        logger.info("Database connected")
    except Exception as e:
        logger.warning(f"Database connection failed: {e}")
    
    try:
        await redis_client.connect()
        logger.info("Redis connected")
    except Exception as e:
        logger.warning(f"Redis connection failed: {e}")
    
    try:
        await vector_db.connect()
        logger.info("Vector database connected")
    except Exception as e:
        logger.warning(f"Vector database connection failed: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await db.disconnect()
    await redis_client.disconnect()
    await vector_db.disconnect()


app = FastAPI(
    title=settings.app_name,
    description="An adaptive Telugu language learning application",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error_code": "INTERNAL_ERROR",
            "message": "An unexpected error occurred",
        },
    )


# Include API routes
app.include_router(api_router, prefix="/api/v1")


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.app_name}
