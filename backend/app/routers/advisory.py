"""
MonSense Advisory API Router
Endpoints for crop-specific advisories.
— Dr. Meenakshi Iyer (Agricultural Scientist)
— Kabir Mehra (LLM & Prompt Engineering Integrator)
"""

from datetime import date, timedelta
from typing import Optional, List
from fastapi import APIRouter, Query, HTTPException
from app.ml.forecast_engine import forecast_engine
from app.ml.advisory_engine import advisory_engine, CROP_DATABASE
from app.services.location_service import location_service

router = APIRouter(prefix="/advisory", tags=["Crop Advisory"])


@router.get("/crops")
async def list_crops():
    """List all supported crops with metadata."""
    crops = []
    for key, crop in CROP_DATABASE.items():
        crops.append({
            "id": key,
            "name": key.title(),
            "name_hi": crop["name_hi"],
            "optimal_rainfall_mm": crop["optimal_rainfall_mm"],
            "drought_tolerance": crop["drought_tolerance"],
            "waterlog_tolerance": crop["waterlog_tolerance"],
            "sowing_months": crop["sowing_months"],
        })
    return {"total": len(crops), "crops": crops}


@router.get("/generate/{location_code}")
async def generate_advisory(
    location_code: str,
    crops: str = Query(default="rice,wheat,cotton,soybean"),
    lead_days: int = Query(default=7, ge=1, le=30),
):
    """Generate crop-specific advisories for a location."""
    location = location_service.get_by_code(location_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location '{location_code}' not found")

    target_date = date.today() + timedelta(days=lead_days)

    # Get forecast
    forecast = await forecast_engine.predict(
        location_code=location["code"],
        state_name=location.get("state_name", "Maharashtra"),
        latitude=location.get("latitude", 19.0),
        longitude=location.get("longitude", 73.0),
        elevation_m=location.get("elevation_m", 500),
        target_date=target_date,
        lead_days=lead_days,
    )

    # Generate advisories for specified crops
    crop_list = [c.strip().lower() for c in crops.split(",")]
    advisories = advisory_engine.generate_multi_crop_advisory(crop_list, forecast)

    return {
        "location": {
            "name": location["name"],
            "code": location["code"],
            "district": location.get("district_name"),
        },
        "forecast_summary": {
            "target_date": target_date.isoformat(),
            "predicted_rainfall_mm": forecast["predicted_rainfall_mm"],
            "risk_category": forecast["risk_category"],
            "heavy_rainfall_prob": forecast["heavy_rainfall_prob"],
            "dry_spell_prob": forecast["dry_spell_prob"],
        },
        "total_advisories": len(advisories),
        "advisories": advisories,
    }


@router.get("/bulk/{district_code}")
async def generate_bulk_advisories(
    district_code: str,
    crops: str = Query(default="rice,soybean"),
    lead_days: int = Query(default=7, ge=1, le=30),
):
    """Generate advisories for all blocks in a district."""
    location = location_service.get_by_code(district_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"District '{district_code}' not found")

    blocks = location_service.get_children(location["id"])
    target_date = date.today() + timedelta(days=lead_days)
    crop_list = [c.strip().lower() for c in crops.split(",")]

    results = []
    for block in blocks:
        forecast = await forecast_engine.predict(
            location_code=block["code"],
            state_name=block.get("state_name", "Maharashtra"),
            latitude=block.get("latitude", 19.0),
            longitude=block.get("longitude", 73.0),
            elevation_m=block.get("elevation_m", 500),
            target_date=target_date,
            lead_days=lead_days,
        )
        advisories = advisory_engine.generate_multi_crop_advisory(crop_list, forecast)

        results.append({
            "block_name": block["name"],
            "block_code": block["code"],
            "risk_category": forecast["risk_category"],
            "rainfall_mm": forecast["predicted_rainfall_mm"],
            "advisories": advisories,
        })

    return {
        "district": location["name"],
        "target_date": target_date.isoformat(),
        "total_blocks": len(results),
        "blocks": results,
    }


@router.post("/simulate")
async def simulate_advisory_scenario(
    rainfall_mm: float = Query(default=65.0, ge=0.0, le=500.0),
    dry_spell_days: int = Query(default=2, ge=0, le=60),
    crop: str = Query(default="rice"),
    crop_stage: str = Query(default="flowering"),
    heavy_rainfall_prob: Optional[float] = None,
    flood_risk_prob: Optional[float] = None,
    lead_days: int = Query(default=7, ge=1, le=30),
):
    """Simulate crop-specific advisories based on hypothetical forecast parameters."""
    advisories = advisory_engine.simulate_from_params(
        rainfall_mm=rainfall_mm,
        dry_spell_days=dry_spell_days,
        crop=crop,
        crop_stage=crop_stage,
        heavy_rainfall_prob=heavy_rainfall_prob or 0.0,
        flood_risk_prob=flood_risk_prob or 0.0,
        lead_days=lead_days,
    )
    return {
        "simulation_parameters": {
            "rainfall_mm": rainfall_mm,
            "dry_spell_days": dry_spell_days,
            "crop": crop,
            "crop_stage": crop_stage,
            "lead_days": lead_days,
        },
        "total_advisories": len(advisories),
        "advisories": advisories,
    }

