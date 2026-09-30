"""
MonSense Alert Service
Handles SMS and WhatsApp alert dispatching via Twilio/GupShup.
— Manish Tiwari (Rural Communication & Telecom API Lead)
— Alok Varma (IoT & Weather Station Fallback Engineer)
"""

from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


# Demo farmer database
DEMO_FARMERS = [
    {
        "id": "f0000001-0000-0000-0000-000000000001",
        "name": "Ramesh Patil",
        "phone": "+919876543210",
        "location_id": "c0000001-0000-0000-0000-000000000001",  # Baramati
        "language_preference": "hi",
        "crops": ["soybean", "cotton"],
        "alert_channels": ["sms", "whatsapp"],
    },
    {
        "id": "f0000002-0000-0000-0000-000000000001",
        "name": "Sunita Jadhav",
        "phone": "+919876543211",
        "location_id": "c0000001-0000-0000-0000-000000000001",  # Baramati
        "language_preference": "hi",
        "crops": ["sugarcane", "rice"],
        "alert_channels": ["sms"],
    },
    {
        "id": "f0000003-0000-0000-0000-000000000001",
        "name": "Ganesh Deshmukh",
        "phone": "+919876543212",
        "location_id": "c0000002-0000-0000-0000-000000000001",  # Indapur
        "language_preference": "hi",
        "crops": ["wheat", "groundnut"],
        "alert_channels": ["sms", "whatsapp"],
    },
    {
        "id": "f0000004-0000-0000-0000-000000000001",
        "name": "Lakshmi Bhosale",
        "phone": "+919876543213",
        "location_id": "c0000003-0000-0000-0000-000000000001",  # Junnar
        "language_preference": "hi",
        "crops": ["rice", "pulses"],
        "alert_channels": ["sms"],
    },
    {
        "id": "f0000005-0000-0000-0000-000000000001",
        "name": "Ashok More",
        "phone": "+919876543214",
        "location_id": "c0000007-0000-0000-0000-000000000001",  # Nagpur Rural
        "language_preference": "hi",
        "crops": ["cotton", "soybean", "maize"],
        "alert_channels": ["sms", "whatsapp"],
    },
]


class AlertService:
    """Manages alert dispatching.
    In production, integrates with Twilio for SMS and GupShup for WhatsApp.
    For MVP demo, simulates sending and logs results."""

    def __init__(self):
        self.farmers = {f["id"]: f for f in DEMO_FARMERS}
        self.sent_alerts: List[Dict] = []

    def get_farmers(self, location_id: Optional[str] = None) -> List[Dict]:
        """Get registered farmers, optionally by location."""
        farmers = list(self.farmers.values())
        if location_id:
            farmers = [f for f in farmers if f["location_id"] == location_id]
        return farmers

    def get_farmer_by_id(self, farmer_id: str) -> Optional[Dict]:
        """Get farmer by ID."""
        return self.farmers.get(farmer_id)

    async def send_sms(
        self,
        phone: str,
        message: str,
        language: str = "hi",
    ) -> Dict:
        """Send SMS alert (simulated for demo)."""
        alert = {
            "channel": "sms",
            "recipient_phone": phone,
            "language": language,
            "message_content": message[:160],  # SMS character limit
            "status": "delivered",
            "external_id": f"SMS-{len(self.sent_alerts) + 1:06d}",
            "sent_at": datetime.utcnow().isoformat(),
        }
        self.sent_alerts.append(alert)
        logger.info(f"SMS sent to {phone}: {message[:50]}...")
        return alert

    async def send_whatsapp(
        self,
        phone: str,
        message: str,
        language: str = "hi",
    ) -> Dict:
        """Send WhatsApp alert (simulated for demo)."""
        alert = {
            "channel": "whatsapp",
            "recipient_phone": phone,
            "language": language,
            "message_content": message,
            "status": "delivered",
            "external_id": f"WA-{len(self.sent_alerts) + 1:06d}",
            "sent_at": datetime.utcnow().isoformat(),
        }
        self.sent_alerts.append(alert)
        logger.info(f"WhatsApp sent to {phone}: {message[:50]}...")
        return alert

    async def send_alert(
        self,
        phone: str,
        message: str,
        channel: str = "sms",
        language: str = "hi",
    ) -> Dict:
        """Send alert via specified channel."""
        if channel == "whatsapp":
            return await self.send_whatsapp(phone, message, language)
        else:
            return await self.send_sms(phone, message, language)

    async def broadcast_to_location(
        self,
        location_id: str,
        message_en: str,
        message_hi: str,
        channel: str = "sms",
    ) -> List[Dict]:
        """Broadcast alert to all farmers in a location."""
        farmers = self.get_farmers(location_id)
        results = []
        for farmer in farmers:
            lang = farmer.get("language_preference", "hi")
            message = message_hi if lang == "hi" else message_en

            if channel in farmer.get("alert_channels", ["sms"]):
                result = await self.send_alert(
                    farmer["phone"], message, channel, lang
                )
                result["farmer_name"] = farmer["name"]
                results.append(result)
        return results

    def get_alert_stats(self) -> Dict:
        """Get alert delivery statistics."""
        total = len(self.sent_alerts)
        sms_count = sum(1 for a in self.sent_alerts if a["channel"] == "sms")
        wa_count = sum(1 for a in self.sent_alerts if a["channel"] == "whatsapp")
        delivered = sum(1 for a in self.sent_alerts if a["status"] == "delivered")

        return {
            "total_alerts": total,
            "sms_sent": sms_count,
            "whatsapp_sent": wa_count,
            "delivered": delivered,
            "failed": total - delivered,
            "delivery_rate": f"{(delivered / total * 100):.1f}%" if total > 0 else "N/A",
        }

    def get_recent_alerts(self, limit: int = 20) -> List[Dict]:
        """Get most recent alerts."""
        return self.sent_alerts[-limit:]


# Singleton
alert_service = AlertService()
