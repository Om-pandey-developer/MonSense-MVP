"""
MonSense Database Models
PostGIS-enabled spatial models for locations, forecasts, and advisories.
— Priya Nair (Data Engineering & Spatial Pipeline Lead)
— Karan Malhotra (Database Administrator)
"""

import uuid
from datetime import datetime, date
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, Date, Text,
    ForeignKey, Boolean, Enum as SAEnum, JSON, Index
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.database import Base
import enum


# ─── Enums ───────────────────────────────────────────────────────────────

class LocationLevel(str, enum.Enum):
    STATE = "state"
    DISTRICT = "district"
    BLOCK = "block"
    VILLAGE = "village"
    PANCHAYAT = "panchayat"


class RiskCategory(str, enum.Enum):
    VERY_LOW = "very_low"       # 0-10%
    LOW = "low"                  # 10-30%
    MODERATE = "moderate"        # 30-50%
    HIGH = "high"                # 50-70%
    VERY_HIGH = "very_high"      # 70-100%


class AlertChannel(str, enum.Enum):
    SMS = "sms"
    WHATSAPP = "whatsapp"
    IVR = "ivr"
    APP = "app"


class CropStage(str, enum.Enum):
    PRE_SOWING = "pre_sowing"
    SOWING = "sowing"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    MATURITY = "maturity"
    HARVEST = "harvest"


# ─── Location Model ─────────────────────────────────────────────────────

class Location(Base):
    """Hierarchical geographic location with PostGIS geometry."""
    __tablename__ = "locations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False, index=True)
    name_local = Column(String(255))  # Local language name
    code = Column(String(50), unique=True, nullable=False)  # LGD code
    level = Column(SAEnum(LocationLevel), nullable=False, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=True)
    state_name = Column(String(255), index=True)
    district_name = Column(String(255), index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation_m = Column(Float)
    area_sq_km = Column(Float)
    geometry = Column(Geometry("MULTIPOLYGON", srid=4326))
    centroid = Column(Geometry("POINT", srid=4326))
    population = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    parent = relationship("Location", remote_side=[id], backref="children")
    forecasts = relationship("Forecast", back_populates="location")
    advisories = relationship("CropAdvisory", back_populates="location")

    __table_args__ = (
        Index("idx_location_geometry", "geometry", postgresql_using="gist"),
        Index("idx_location_level_state", "level", "state_name"),
    )


# ─── Climate Index Model ────────────────────────────────────────────────

class ClimateIndex(Base):
    """Teleconnection indices: ENSO (Niño 3.4 SST), IOD (DMI), MJO (RMM)."""
    __tablename__ = "climate_indices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    index_date = Column(Date, nullable=False, index=True)
    enso_nino34 = Column(Float)        # Niño 3.4 SST anomaly
    enso_phase = Column(String(20))     # El Niño / La Niña / Neutral
    iod_dmi = Column(Float)            # Dipole Mode Index
    iod_phase = Column(String(20))      # Positive / Negative / Neutral
    mjo_phase = Column(Integer)         # MJO phase 1-8
    mjo_amplitude = Column(Float)       # RMM amplitude
    source = Column(String(100))        # Data source attribution
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_climate_date", "index_date"),
    )


# ─── Weather Observation Model ──────────────────────────────────────────

class WeatherObservation(Base):
    """Gridded weather observation from IMD/ERA5/GPM-IMERG."""
    __tablename__ = "weather_observations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    observation_date = Column(Date, nullable=False, index=True)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    rainfall_mm = Column(Float)
    temperature_max_c = Column(Float)
    temperature_min_c = Column(Float)
    humidity_pct = Column(Float)
    wind_speed_kmh = Column(Float)
    wind_direction_deg = Column(Float)
    pressure_hpa = Column(Float)
    cloud_cover_pct = Column(Float)
    soil_moisture = Column(Float)
    source = Column(String(50))  # IMD, ERA5, GPM-IMERG
    grid_resolution_deg = Column(Float)  # e.g., 0.25 for 25km
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_obs_date_location", "observation_date", "location_id"),
    )


# ─── Forecast Model ─────────────────────────────────────────────────────

class Forecast(Base):
    """Block/village-level rainfall forecast with probability risk levels."""
    __tablename__ = "forecasts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    forecast_date = Column(Date, nullable=False, index=True)
    target_date = Column(Date, nullable=False, index=True)
    lead_days = Column(Integer, nullable=False)

    # Rainfall prediction
    predicted_rainfall_mm = Column(Float, nullable=False)
    rainfall_lower_bound = Column(Float)
    rainfall_upper_bound = Column(Float)
    prediction_confidence = Column(Float)

    # Risk probabilities (0-100%)
    heavy_rainfall_prob = Column(Float, default=0.0)
    dry_spell_prob = Column(Float, default=0.0)
    monsoon_onset_prob = Column(Float, default=0.0)
    flood_risk_prob = Column(Float, default=0.0)

    # Categorized risk
    risk_category = Column(SAEnum(RiskCategory), nullable=False)

    # Model metadata
    model_version = Column(String(50))
    model_type = Column(String(50))  # LSTM, XGBoost, Ensemble
    feature_importance = Column(JSON)

    # Climate indices used
    enso_value = Column(Float)
    iod_value = Column(Float)
    mjo_phase = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    location = relationship("Location", back_populates="forecasts")

    __table_args__ = (
        Index("idx_forecast_location_target", "location_id", "target_date"),
        Index("idx_forecast_risk", "risk_category", "target_date"),
    )


# ─── Crop Advisory Model ────────────────────────────────────────────────

class CropAdvisory(Base):
    """Crop-specific advisory generated by the rule engine."""
    __tablename__ = "crop_advisories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"), nullable=False)
    forecast_id = Column(UUID(as_uuid=True), ForeignKey("forecasts.id"), nullable=False)
    advisory_date = Column(Date, nullable=False, index=True)

    crop_name = Column(String(100), nullable=False)
    crop_stage = Column(SAEnum(CropStage))
    advisory_type = Column(String(100))  # delay_sowing, irrigate, harvest_early, etc.
    advisory_text_en = Column(Text, nullable=False)
    advisory_text_hi = Column(Text)      # Hindi
    advisory_text_local = Column(Text)    # Regional language
    severity = Column(String(20))         # info, warning, critical
    actions = Column(JSON)                # Structured action items

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)

    # Relationships
    location = relationship("Location", back_populates="advisories")
    forecast = relationship("Forecast")

    __table_args__ = (
        Index("idx_advisory_location_date", "location_id", "advisory_date"),
    )


# ─── Alert Log Model ────────────────────────────────────────────────────

class AlertLog(Base):
    """Log of all alerts sent via SMS/WhatsApp/IVR."""
    __tablename__ = "alert_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    advisory_id = Column(UUID(as_uuid=True), ForeignKey("crop_advisories.id"))
    recipient_phone = Column(String(20), nullable=False)
    recipient_name = Column(String(255))
    channel = Column(SAEnum(AlertChannel), nullable=False)
    language = Column(String(10), default="en")
    message_content = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, sent, delivered, failed
    external_id = Column(String(255))  # Twilio/GupShup message ID
    error_message = Column(Text)
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_alert_status", "status", "channel"),
    )


# ─── User/Farmer Model ──────────────────────────────────────────────────

class Farmer(Base):
    """Registered farmer for receiving alerts."""
    __tablename__ = "farmers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    location_id = Column(UUID(as_uuid=True), ForeignKey("locations.id"))
    language_preference = Column(String(10), default="hi")
    crops = Column(ARRAY(String))  # List of crops grown
    land_area_hectares = Column(Float)
    alert_channels = Column(ARRAY(String), default=["sms"])
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    location = relationship("Location")
