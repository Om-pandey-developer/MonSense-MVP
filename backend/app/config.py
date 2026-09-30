"""
MonSense Backend Configuration
Manages environment variables and application settings.
— Amitabh Bannerjee (Cybersecurity & Data Privacy Officer)
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # App
    APP_NAME: str = "MonSense"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "monsense-dev-secret-key-change-in-production"
    API_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://monsense:monsense@localhost:5432/monsense_db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 300  # 5 minutes

    # ML Model
    MODEL_PATH: str = "ml/models"
    LSTM_MODEL_FILE: str = "lstm_rainfall.h5"
    XGBOOST_MODEL_FILE: str = "xgboost_downscale.joblib"
    INFERENCE_TIMEOUT: int = 30

    # External Data APIs
    IMD_API_URL: str = "https://api.imd.gov.in/v1"
    ERA5_CDS_URL: str = "https://cds.climate.copernicus.eu/api/v2"
    GPM_IMERG_URL: str = "https://gpm1.gesdisc.eosdis.nasa.gov"
    CDS_API_KEY: Optional[str] = None

    # Alert Services
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    GUPSHUP_API_KEY: Optional[str] = None
    GUPSHUP_APP_NAME: Optional[str] = None

    # GeoServer
    GEOSERVER_URL: str = "http://localhost:8080/geoserver"
    GEOSERVER_WORKSPACE: str = "monsense"

    # Forecast Settings
    FORECAST_HORIZON_DAYS: int = 30
    SPATIAL_RESOLUTION_KM: float = 4.0
    RISK_THRESHOLDS: str = "10,30,50,70"  # Very Low, Low, Moderate, High, Very High

    @property
    def risk_threshold_list(self) -> list[int]:
        return [int(x) for x in self.RISK_THRESHOLDS.split(",")]

    @property
    def allowed_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
