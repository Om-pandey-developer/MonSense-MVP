"""
MonSense Pydantic Schemas
Request/response validation schemas for all API endpoints.
— Vikramaditya Roy (Backend Systems Architect)
"""

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum


# ─── Enums ───────────────────────────────────────────────────────────────

class LocationLevelEnum(str, Enum):
    STATE = "state"
    DISTRICT = "district"
    BLOCK = "block"
    VILLAGE = "village"
    PANCHAYAT = "panchayat"


class RiskCategoryEnum(str, Enum):
    VERY_LOW = "very_low"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class AlertChannelEnum(str, Enum):
    SMS = "sms"
    WHATSAPP = "whatsapp"
    IVR = "ivr"
    APP = "app"


# ─── Location Schemas ───────────────────────────────────────────────────

class LocationBase(BaseModel):
    name: str
    name_local: Optional[str] = None
    code: str
    level: LocationLevelEnum
    parent_id: Optional[UUID] = None
    state_name: Optional[str] = None
    district_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    elevation_m: Optional[float] = None
    area_sq_km: Optional[float] = None


class LocationCreate(LocationBase):
    pass


class LocationResponse(LocationBase):
    id: UUID
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class LocationGeoJSON(BaseModel):
    """GeoJSON feature for map rendering."""
    type: str = "Feature"
    properties: dict
    geometry: dict


# ─── Climate Index Schemas ───────────────────────────────────────────────

class ClimateIndexResponse(BaseModel):
    id: UUID
    index_date: date
    enso_nino34: Optional[float] = None
    enso_phase: Optional[str] = None
    iod_dmi: Optional[float] = None
    iod_phase: Optional[str] = None
    mjo_phase: Optional[int] = None
    mjo_amplitude: Optional[float] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Forecast Schemas ────────────────────────────────────────────────────

class ForecastRequest(BaseModel):
    location_id: UUID
    target_date: date
    lead_days: int = Field(ge=1, le=30)


class ForecastResponse(BaseModel):
    id: UUID
    location_id: UUID
    location_name: Optional[str] = None
    forecast_date: date
    target_date: date
    lead_days: int
    predicted_rainfall_mm: float
    rainfall_lower_bound: Optional[float] = None
    rainfall_upper_bound: Optional[float] = None
    prediction_confidence: Optional[float] = None
    heavy_rainfall_prob: float = 0.0
    dry_spell_prob: float = 0.0
    monsoon_onset_prob: float = 0.0
    flood_risk_prob: float = 0.0
    risk_category: RiskCategoryEnum
    model_version: Optional[str] = None
    model_type: Optional[str] = None
    enso_value: Optional[float] = None
    iod_value: Optional[float] = None
    mjo_phase: Optional[int] = None

    class Config:
        from_attributes = True


class ForecastSummary(BaseModel):
    """Aggregated forecast summary for a region."""
    location_name: str
    total_locations: int
    date_range: dict
    avg_rainfall_mm: float
    risk_distribution: dict  # {risk_category: count}
    heavy_rainfall_alerts: int
    dry_spell_alerts: int


class RiskMapFeature(BaseModel):
    """Single feature for the risk heatmap GeoJSON layer."""
    type: str = "Feature"
    properties: dict  # risk_category, rainfall_mm, probability, etc.
    geometry: dict    # GeoJSON geometry


class RiskMapGeoJSON(BaseModel):
    """Complete GeoJSON FeatureCollection for the risk heatmap."""
    type: str = "FeatureCollection"
    features: List[RiskMapFeature]
    metadata: dict


# ─── Advisory Schemas ────────────────────────────────────────────────────

class CropAdvisoryResponse(BaseModel):
    id: UUID
    location_id: UUID
    location_name: Optional[str] = None
    advisory_date: date
    crop_name: str
    crop_stage: Optional[str] = None
    advisory_type: Optional[str] = None
    advisory_text_en: str
    advisory_text_hi: Optional[str] = None
    advisory_text_local: Optional[str] = None
    severity: Optional[str] = None
    actions: Optional[dict] = None
    is_active: bool
    forecast: Optional[ForecastResponse] = None

    class Config:
        from_attributes = True


# ─── Alert Schemas ───────────────────────────────────────────────────────

class AlertRequest(BaseModel):
    advisory_id: UUID
    recipient_phone: str
    channel: AlertChannelEnum = AlertChannelEnum.SMS
    language: str = "hi"


class AlertResponse(BaseModel):
    id: UUID
    advisory_id: Optional[UUID] = None
    recipient_phone: str
    channel: AlertChannelEnum
    language: str
    message_content: str
    status: str
    external_id: Optional[str] = None
    sent_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BulkAlertRequest(BaseModel):
    location_id: UUID
    advisory_id: UUID
    channel: AlertChannelEnum = AlertChannelEnum.SMS
    language: str = "hi"


# ─── Farmer Schemas ──────────────────────────────────────────────────────

class FarmerCreate(BaseModel):
    name: str
    phone: str
    location_id: Optional[UUID] = None
    language_preference: str = "hi"
    crops: Optional[List[str]] = None
    land_area_hectares: Optional[float] = None
    alert_channels: List[str] = ["sms"]


class FarmerResponse(BaseModel):
    id: UUID
    name: str
    phone: str
    location_id: Optional[UUID] = None
    language_preference: str
    crops: Optional[List[str]] = None
    land_area_hectares: Optional[float] = None
    alert_channels: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Dashboard Schemas ──────────────────────────────────────────────────

class DashboardStats(BaseModel):
    """Aggregated stats for the dashboard overview."""
    total_locations: int
    active_forecasts: int
    active_advisories: int
    alerts_sent_today: int
    high_risk_blocks: int
    registered_farmers: int
    monsoon_status: str  # onset, active, retreat, off-season
    current_enso: Optional[str] = None
    current_iod: Optional[str] = None
    current_mjo_phase: Optional[int] = None


class TimeSeriesPoint(BaseModel):
    """Single point in a time-series chart."""
    date: date
    value: float
    label: Optional[str] = None


class ForecastTimeSeries(BaseModel):
    """Time-series data for forecast charts."""
    location_name: str
    parameter: str  # rainfall, temperature, etc.
    unit: str
    data: List[TimeSeriesPoint]
    prediction_start: date


# ─── Simulation Schemas ──────────────────────────────────────────────────

class AdvisorySimulationRequest(BaseModel):
    """Payload for interactive crop scenario advisory simulation."""
    rainfall_mm: float = Field(default=65.0, ge=0.0, le=500.0)
    dry_spell_days: int = Field(default=2, ge=0, le=60)
    crop: str = Field(default="rice")
    crop_stage: str = Field(default="flowering")
    heavy_rainfall_prob: Optional[float] = None
    flood_risk_prob: Optional[float] = None
    lead_days: int = Field(default=7, ge=1, le=30)


class BroadcastSimulationRequest(BaseModel):
    """Payload for mobile alert dispatch simulation."""
    district_code: str = Field(default="MH-PUN")
    channel: str = Field(default="all")
    lead_days: int = Field(default=2, ge=1, le=14)

