"""
MonSense Dashboard API Router
Aggregated endpoints for the frontend dashboard.
— Vikramaditya Roy (Backend Systems Architect)
"""

from datetime import date, timedelta
from fastapi import APIRouter
from app.services.location_service import location_service
from app.services.alert_service import alert_service
from app.ml.forecast_engine import forecast_engine, ClimateIndices

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats")
async def get_dashboard_stats():
    """Get overview statistics for the dashboard."""
    all_locations = location_service.get_all()
    blocks = location_service.get_all(level="block")
    farmers = alert_service.get_farmers()
    alert_stats = alert_service.get_alert_stats()

    # Determine monsoon status based on month
    month = date.today().month
    if month in (6, 7, 8, 9):
        monsoon_status = "active"
    elif month == 5:
        monsoon_status = "onset"
    elif month == 10:
        monsoon_status = "retreat"
    else:
        monsoon_status = "off-season"

    # Get current climate indices
    enso_val, enso_phase = ClimateIndices.get_enso_nino34(date.today())
    iod_val, iod_phase = ClimateIndices.get_iod_dmi(date.today())
    mjo_phase, mjo_amp = ClimateIndices.get_mjo(date.today())

    # Count high risk blocks
    target_date = date.today() + timedelta(days=7)
    predictions = await forecast_engine.predict_batch(blocks, target_date)
    high_risk = sum(
        1 for p in predictions
        if p.get("risk_category") in ("high", "very_high")
    )

    return {
        "total_locations": len(all_locations),
        "total_districts": len(location_service.get_all(level="district")),
        "total_blocks": len(blocks),
        "total_villages": len(location_service.get_all(level="village")),
        "registered_farmers": len(farmers),
        "active_forecasts": len(predictions),
        "active_advisories": sum(1 for p in predictions if p.get("risk_category") != "very_low"),
        "alerts_sent_today": alert_stats.get("total_alerts", 0),
        "high_risk_blocks": high_risk,
        "monsoon_status": monsoon_status,
        "climate_indices": {
            "enso": {
                "nino34": enso_val,
                "phase": enso_phase,
            },
            "iod": {
                "dmi": iod_val,
                "phase": iod_phase,
            },
            "mjo": {
                "phase": mjo_phase,
                "amplitude": mjo_amp,
            },
        },
    }


@router.get("/risk-overview")
async def get_risk_overview():
    """Get risk distribution across all blocks."""
    blocks = location_service.get_all(level="block")
    target_date = date.today() + timedelta(days=7)
    predictions = await forecast_engine.predict_batch(blocks, target_date)

    distribution = {"very_low": 0, "low": 0, "moderate": 0, "high": 0, "very_high": 0}
    block_risks = []

    for pred in predictions:
        risk = pred.get("risk_category", "low")
        distribution[risk] += 1
        block_risks.append({
            "name": pred.get("location_name"),
            "code": pred.get("location_code"),
            "risk": risk,
            "rainfall_mm": pred.get("predicted_rainfall_mm"),
            "heavy_prob": pred.get("heavy_rainfall_prob"),
        })

    # Sort by risk severity
    risk_order = {"very_high": 0, "high": 1, "moderate": 2, "low": 3, "very_low": 4}
    block_risks.sort(key=lambda x: risk_order.get(x["risk"], 5))

    return {
        "target_date": target_date.isoformat(),
        "distribution": distribution,
        "blocks": block_risks,
    }


@router.get("/recent-activity")
async def get_recent_activity():
    """Get recent system activity for the dashboard feed."""
    alerts = alert_service.get_recent_alerts(10)

    activities = []

    # Add forecast activities
    blocks = location_service.get_all(level="block")[:5]
    for block in blocks:
        activities.append({
            "type": "forecast",
            "message": f"Forecast updated for {block['name']} block",
            "timestamp": date.today().isoformat(),
            "icon": "🌧️",
        })

    # Add alert activities
    for alert in alerts[:5]:
        activities.append({
            "type": "alert",
            "message": f"Alert sent to {alert.get('recipient_phone', 'N/A')} via {alert.get('channel', 'sms').upper()}",
            "timestamp": alert.get("sent_at", date.today().isoformat()),
            "icon": "📱" if alert.get("channel") == "sms" else "💬",
        })

    return {"activities": activities[:15]}
