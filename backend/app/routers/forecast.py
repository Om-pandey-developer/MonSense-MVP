"""
MonSense Forecast API Router
Endpoints for rainfall predictions, risk maps, and time-series data.
— Vikramaditya Roy (Backend Systems Architect)
"""

from datetime import date, timedelta
from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.ml.forecast_engine import forecast_engine
from app.ml.advisory_engine import advisory_engine
from app.services.location_service import location_service

router = APIRouter(prefix="/forecast", tags=["Forecast"])


@router.get("/predict/{location_code}")
async def get_forecast(
    location_code: str,
    target_date: Optional[date] = None,
    lead_days: int = Query(default=7, ge=1, le=30),
):
    """Get rainfall forecast for a specific location."""
    location = location_service.get_by_code(location_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location '{location_code}' not found")

    if target_date is None:
        target_date = date.today() + timedelta(days=lead_days)

    prediction = await forecast_engine.predict(
        location_code=location["code"],
        state_name=location.get("state_name", "Maharashtra"),
        latitude=location.get("latitude", 19.0),
        longitude=location.get("longitude", 73.0),
        elevation_m=location.get("elevation_m", 500),
        target_date=target_date,
        lead_days=lead_days,
    )

    prediction["location"] = {
        "id": location["id"],
        "name": location["name"],
        "code": location["code"],
        "level": location["level"],
        "latitude": location.get("latitude"),
        "longitude": location.get("longitude"),
    }
    prediction["forecast_date"] = date.today().isoformat()
    prediction["target_date"] = target_date.isoformat()
    prediction["lead_days"] = lead_days

    return prediction


@router.get("/time-series/{location_code}")
async def get_time_series(
    location_code: str,
    days: int = Query(default=30, ge=7, le=60),
):
    """Get multi-day forecast time series for charts."""
    location = location_service.get_by_code(location_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location '{location_code}' not found")

    series = await forecast_engine.get_time_series(
        location_code=location["code"],
        state_name=location.get("state_name", "Maharashtra"),
        latitude=location.get("latitude", 19.0),
        longitude=location.get("longitude", 73.0),
        elevation_m=location.get("elevation_m", 500),
        days=days,
    )

    return {
        "location": {
            "name": location["name"],
            "code": location["code"],
        },
        "parameter": "rainfall",
        "unit": "mm/day",
        "forecast_start": date.today().isoformat(),
        "data": series,
    }


@router.get("/risk-map")
async def get_risk_map(
    target_date: Optional[date] = None,
    level: str = Query(default="block", regex="^(district|block|village)$"),
    district_id: Optional[str] = None,
):
    """Get GeoJSON risk map for all locations at specified level."""
    if target_date is None:
        target_date = date.today() + timedelta(days=7)

    # Get locations at the requested level
    if district_id:
        locations = location_service.get_children(district_id)
        locations = [l for l in locations if l["level"] == level]
    else:
        locations = location_service.get_all(level=level)

    if not locations:
        locations = location_service.get_all(level="block")

    # Generate forecasts for all locations
    predictions = await forecast_engine.predict_batch(locations, target_date)

    # Build GeoJSON FeatureCollection
    features = []
    risk_counts = {"very_low": 0, "low": 0, "moderate": 0, "high": 0, "very_high": 0}

    for pred in predictions:
        risk = pred.get("risk_category", "low")
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

        # Create a circle-like polygon around the point for visualization
        lat = next((l["latitude"] for l in locations if l["id"] == pred["location_id"]), 19.0)
        lon = next((l["longitude"] for l in locations if l["id"] == pred["location_id"]), 73.0)

        # Generate a simple bounding box polygon (in production, use actual boundary GeoJSON)
        delta = 0.15  # ~15km box
        feature = {
            "type": "Feature",
            "properties": {
                "location_id": pred["location_id"],
                "location_name": pred["location_name"],
                "location_code": pred["location_code"],
                "rainfall_mm": pred["predicted_rainfall_mm"],
                "heavy_rainfall_prob": pred["heavy_rainfall_prob"],
                "dry_spell_prob": pred["dry_spell_prob"],
                "flood_risk_prob": pred["flood_risk_prob"],
                "risk_category": risk,
                "target_date": pred["target_date"],
                "confidence": pred.get("prediction_confidence", 0),
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [lon - delta, lat - delta],
                    [lon + delta, lat - delta],
                    [lon + delta, lat + delta],
                    [lon - delta, lat + delta],
                    [lon - delta, lat - delta],
                ]],
            },
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features,
        "metadata": {
            "target_date": target_date.isoformat(),
            "level": level,
            "total_locations": len(features),
            "risk_distribution": risk_counts,
            "generated_at": date.today().isoformat(),
        },
    }


@router.get("/summary/{district_code}")
async def get_district_summary(
    district_code: str,
    days: int = Query(default=7, ge=1, le=30),
):
    """Get aggregated forecast summary for a district."""
    location = location_service.get_by_code(district_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"District '{district_code}' not found")

    blocks = location_service.get_children(location["id"])
    target_date = date.today() + timedelta(days=days)

    predictions = await forecast_engine.predict_batch(blocks, target_date)

    # Aggregate
    risk_dist = {"very_low": 0, "low": 0, "moderate": 0, "high": 0, "very_high": 0}
    total_rainfall = 0
    heavy_alerts = 0
    dry_alerts = 0

    for pred in predictions:
        risk_dist[pred.get("risk_category", "low")] += 1
        total_rainfall += pred.get("predicted_rainfall_mm", 0)
        if pred.get("heavy_rainfall_prob", 0) > 50:
            heavy_alerts += 1
        if pred.get("dry_spell_prob", 0) > 50:
            dry_alerts += 1

    avg_rainfall = total_rainfall / len(predictions) if predictions else 0

    return {
        "location_name": location["name"],
        "total_blocks": len(blocks),
        "date_range": {
            "start": date.today().isoformat(),
            "end": target_date.isoformat(),
        },
        "avg_rainfall_mm": round(avg_rainfall, 1),
        "risk_distribution": risk_dist,
        "heavy_rainfall_alerts": heavy_alerts,
        "dry_spell_alerts": dry_alerts,
        "climate_indices": {
            "enso": predictions[0].get("enso_value") if predictions else None,
            "enso_phase": predictions[0].get("enso_phase") if predictions else None,
            "iod": predictions[0].get("iod_value") if predictions else None,
            "mjo_phase": predictions[0].get("mjo_phase") if predictions else None,
        },
    }
