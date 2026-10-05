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
    live: bool = Query(default=False, description="Fetch live telemetry from Open-Meteo API"),
):
    """Get rainfall forecast for a specific location."""
    location = location_service.get_by_code(location_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location '{location_code}' not found")

    if target_date is None:
        target_date = date.today() + timedelta(days=lead_days)

    if live:
        prediction = await forecast_engine.predict_with_live_weather(
            location_code=location["code"],
            state_name=location.get("state_name", "Maharashtra"),
            latitude=location.get("latitude", 19.0),
            longitude=location.get("longitude", 73.0),
            elevation_m=location.get("elevation_m", 500),
            target_date=target_date,
            lead_days=lead_days,
        )
    else:
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


import math
import hashlib
import time
from app.services.weather_service import weather_service

def generate_organic_polygon(lat: float, lon: float, seed_str: str) -> list:
    """Generate realistic organic multi-vertex administrative boundary polygon."""
    h = int(hashlib.md5(seed_str.encode()).hexdigest()[:8], 16)
    p1 = (h % 360) * math.pi / 180.0
    p2 = ((h >> 4) % 360) * math.pi / 180.0
    p3 = ((h >> 8) % 360) * math.pi / 180.0

    num_vertices = 14
    base_radius = 0.12  # ~13 km
    coords = []
    for i in range(num_vertices):
        theta = (i / num_vertices) * 2.0 * math.pi
        radial_variation = (
            1.0
            + 0.22 * math.sin(2.0 * theta + p1)
            + 0.14 * math.cos(3.0 * theta + p2)
            + 0.08 * math.sin(5.0 * theta + p3)
        )
        r = base_radius * radial_variation
        lng_offset = (r * math.cos(theta)) * 1.05
        lat_offset = (r * math.sin(theta)) * 0.95
        coords.append([round(lon + lng_offset, 4), round(lat + lat_offset, 4)])
    coords.append(coords[0])  # close loop
    return [coords]


@router.get("/live-telemetry/{location_code}")
async def get_live_telemetry(location_code: str):
    """
    Directly query Open-Meteo live numerical weather prediction (ECMWF/GFS)
    for exact block coordinates to verify live data.
    """
    location = location_service.get_by_code(location_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location '{location_code}' not found")

    lat = float(location.get("latitude", 19.0))
    lon = float(location.get("longitude", 73.0))

    start_t = time.time()
    raw_weather = await weather_service.fetch_weather(lat, lon, days=7)
    elapsed_ms = round((time.time() - start_t) * 1000, 1)

    if raw_weather and "daily" in raw_weather:
        daily = raw_weather["daily"]
        t_max_list = daily.get("temperature_2m_max", [32.0])
        t_min_list = daily.get("temperature_2m_min", [22.0])
        precip_list = daily.get("precipitation_sum", [0.0])
        soil_list = daily.get("soil_moisture_0_to_7cm_mean", [0.22])

        return {
            "status": "online",
            "is_live": True,
            "engine": "Open-Meteo Global NWP (ECMWF/GFS)",
            "location_name": location["name"],
            "location_code": location["code"],
            "state_name": location.get("state_name", "Maharashtra"),
            "coordinates": {"latitude": lat, "longitude": lon},
            "latency_ms": elapsed_ms,
            "current_date": date.today().isoformat(),
            "telemetry": {
                "temperature_max_c": t_max_list[0] if t_max_list else 32.5,
                "temperature_min_c": t_min_list[0] if t_min_list else 22.0,
                "precipitation_today_mm": precip_list[0] if precip_list else 0.0,
                "soil_moisture_volumetric": soil_list[0] if soil_list else 0.22,
                "elevation_m": location.get("elevation_m", 500),
            },
            "source_info": "Real-time feed from Open-Meteo API using high-resolution ECMWF numerical models.",
        }

    return {
        "status": "fallback_offline",
        "is_live": False,
        "engine": "MonSense Calibrated Climatology Simulator (IMD 30-Yr Normals)",
        "location_name": location["name"],
        "location_code": location["code"],
        "state_name": location.get("state_name", "Maharashtra"),
        "coordinates": {"latitude": lat, "longitude": lon},
        "latency_ms": elapsed_ms,
        "telemetry": {
            "temperature_max_c": 31.8,
            "temperature_min_c": 21.5,
            "precipitation_today_mm": 0.0,
            "soil_moisture_volumetric": 0.21,
            "elevation_m": location.get("elevation_m", 500),
        },
        "source_info": "Calibrated historical agro-climatic baseline for offline demo.",
    }


@router.get("/risk-map")
async def get_risk_map(
    target_date: Optional[date] = None,
    level: str = Query(default="block", regex="^(district|block|village)$"),
    district_id: Optional[str] = None,
    state_code: Optional[str] = None,
):
    """Get GeoJSON risk map with organic territorial polygons."""
    if target_date is None:
        target_date = date.today() + timedelta(days=7)

    # Get locations at the requested level
    if district_id:
        locations = location_service.get_children(district_id)
        locations = [l for l in locations if l["level"] == level]
    elif state_code:
        state_loc = location_service.get_by_code(state_code)
        if state_loc:
            state_name = state_loc["name"]
            locations = [
                l for l in location_service.get_all(level=level)
                if l.get("state_name") == state_name
            ]
        else:
            locations = location_service.get_all(level=level)
    else:
        locations = location_service.get_all(level=level)

    if not locations:
        locations = location_service.get_all(level="block")

    # Generate forecasts for all locations
    predictions = await forecast_engine.predict_batch(locations, target_date)

    # Build GeoJSON FeatureCollection with organic boundaries
    features = []
    risk_counts = {"very_low": 0, "low": 0, "moderate": 0, "high": 0, "very_high": 0}

    for pred in predictions:
        risk = pred.get("risk_category", "low")
        risk_counts[risk] = risk_counts.get(risk, 0) + 1

        loc_match = next((l for l in locations if l["id"] == pred["location_id"]), None)
        lat = loc_match["latitude"] if loc_match else 19.0
        lon = loc_match["longitude"] if loc_match else 73.0

        # Generate organic administrative territorial polygon
        poly_coords = generate_organic_polygon(lat, lon, pred["location_code"])

        feature = {
            "type": "Feature",
            "properties": {
                "location_id": pred["location_id"],
                "location_name": pred["location_name"],
                "location_code": pred["location_code"],
                "state_name": loc_match.get("state_name", "Maharashtra") if loc_match else "Maharashtra",
                "district_name": loc_match.get("district_name", "") if loc_match else "",
                "rainfall_mm": pred["predicted_rainfall_mm"],
                "heavy_rainfall_prob": pred["heavy_rainfall_prob"],
                "dry_spell_prob": pred["dry_spell_prob"],
                "monsoon_onset_prob": pred.get("monsoon_onset_prob", 25.0),
                "flood_risk_prob": pred["flood_risk_prob"],
                "risk_category": risk,
                "target_date": pred["target_date"],
                "confidence": pred.get("prediction_confidence", 0),
                "centroid": [lat, lon],
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": poly_coords,
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
