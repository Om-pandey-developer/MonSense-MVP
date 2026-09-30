"""
MonSense Alert API Router
Endpoints for sending SMS/WhatsApp alerts and managing farmers.
— Manish Tiwari (Rural Communication & Telecom API Lead)
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.services.alert_service import alert_service
from app.ml.forecast_engine import forecast_engine
from app.ml.advisory_engine import advisory_engine
from app.services.location_service import location_service
from datetime import date, timedelta

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("/farmers")
async def list_farmers(
    location_id: Optional[str] = None,
):
    """List registered farmers."""
    farmers = alert_service.get_farmers(location_id)
    return {"total": len(farmers), "farmers": farmers}


@router.post("/send")
async def send_alert(
    phone: str,
    message: str,
    channel: str = Query(default="sms", regex="^(sms|whatsapp)$"),
    language: str = "hi",
):
    """Send an alert to a specific phone number."""
    result = await alert_service.send_alert(phone, message, channel, language)
    return result


@router.post("/broadcast/{location_code}")
async def broadcast_alert(
    location_code: str,
    channel: str = Query(default="sms", regex="^(sms|whatsapp)$"),
    crops: str = Query(default="rice,soybean"),
    lead_days: int = Query(default=7, ge=1, le=30),
):
    """Generate advisory and broadcast to all farmers in a location."""
    location = location_service.get_by_code(location_code)
    if not location:
        raise HTTPException(status_code=404, detail=f"Location not found")

    target_date = date.today() + timedelta(days=lead_days)

    # Generate forecast
    forecast = await forecast_engine.predict(
        location_code=location["code"],
        state_name=location.get("state_name", "Maharashtra"),
        latitude=location.get("latitude", 19.0),
        longitude=location.get("longitude", 73.0),
        elevation_m=location.get("elevation_m", 500),
        target_date=target_date,
        lead_days=lead_days,
    )

    # Generate advisories
    crop_list = [c.strip().lower() for c in crops.split(",")]
    advisories = advisory_engine.generate_multi_crop_advisory(crop_list, forecast)

    if not advisories:
        return {"message": "No advisories to broadcast", "alerts_sent": 0}

    # Build alert message from top advisory
    top_advisory = advisories[0]
    message_en = top_advisory["advisory_text_en"]
    message_hi = top_advisory["advisory_text_hi"]

    # Broadcast
    results = await alert_service.broadcast_to_location(
        location["id"], message_en, message_hi, channel
    )

    return {
        "location": location["name"],
        "advisory_type": top_advisory["advisory_type"],
        "risk_category": forecast["risk_category"],
        "alerts_sent": len(results),
        "alerts": results,
    }


@router.get("/stats")
async def get_alert_stats():
    """Get alert delivery statistics."""
    return alert_service.get_alert_stats()


@router.get("/recent")
async def get_recent_alerts(
    limit: int = Query(default=20, ge=1, le=100),
):
    """Get recent alert history."""
    alerts = alert_service.get_recent_alerts(limit)
    return {"total": len(alerts), "alerts": alerts}
