"""
MonSense — Hyperlocal Monsoon Prediction & Crop Advisory Platform
Main FastAPI Application Entry Point.

— Om Pandey (Lead Architect & Project Visionary)
— Vikramaditya Roy (Backend Systems Architect)
— Amitabh Bannerjee (Cybersecurity & Data Privacy Officer)
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.routers import forecast, locations, advisory, alerts, dashboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("monsense")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    logger.info("🌧️  MonSense API starting up...")
    logger.info(f"   Version: {settings.APP_VERSION}")
    logger.info(f"   Debug: {settings.DEBUG}")
    logger.info(f"   CORS: {settings.allowed_origins_list}")
    yield
    logger.info("🌧️  MonSense API shutting down...")


# Create FastAPI application
app = FastAPI(
    title="MonSense API",
    description=(
        "Hyperlocal Monsoon Prediction & Crop Advisory Platform. "
        "Provides block/village-level rainfall forecasts (7-30 day outlook), "
        "color-coded risk probability heatmaps, crop-specific advisories, "
        "and regional language SMS/WhatsApp alerts for Indian farmers."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# ─── Middleware ──────────────────────────────────────────────────────────

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip compression for large GeoJSON payloads
app.add_middleware(GZipMiddleware, minimum_size=1000)


# ─── Routes ──────────────────────────────────────────────────────────────

# Mount all routers under /api/v1
app.include_router(dashboard.router, prefix=settings.API_PREFIX)
app.include_router(forecast.router, prefix=settings.API_PREFIX)
app.include_router(locations.router, prefix=settings.API_PREFIX)
app.include_router(advisory.router, prefix=settings.API_PREFIX)
app.include_router(alerts.router, prefix=settings.API_PREFIX)


# ─── Root & Health Endpoints ─────────────────────────────────────────────

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint — API info."""
    return {
        "name": "MonSense API",
        "version": settings.APP_VERSION,
        "description": "Hyperlocal Monsoon Prediction & Crop Advisory Platform",
        "docs": "/docs",
        "api_prefix": settings.API_PREFIX,
        "endpoints": {
            "dashboard": f"{settings.API_PREFIX}/dashboard/stats",
            "forecast": f"{settings.API_PREFIX}/forecast/predict/{{location_code}}",
            "risk_map": f"{settings.API_PREFIX}/forecast/risk-map",
            "advisory": f"{settings.API_PREFIX}/advisory/generate/{{location_code}}",
            "locations": f"{settings.API_PREFIX}/locations/",
            "alerts": f"{settings.API_PREFIX}/alerts/stats",
        },
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "service": "monsense-api",
        "version": settings.APP_VERSION,
    }
