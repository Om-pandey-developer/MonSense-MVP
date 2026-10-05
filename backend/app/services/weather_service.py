"""
MonSense Weather Service
Fetches live daily weather from Open-Meteo API.
Falls back to synthetic/climatological data on network timeout or failure.
"""

import logging
import httpx
from typing import Dict, Optional
from app.config import get_settings

logger = logging.getLogger(__name__)


class WeatherService:
    """Async weather service integrating Open-Meteo for live telemetry."""

    def __init__(self):
        self.settings = get_settings()
        self.base_url = getattr(self.settings, "OPEN_METEO_URL", "https://api.open-meteo.com/v1/forecast")
        self.timeout = getattr(self.settings, "WEATHER_API_TIMEOUT", 5.0)

    async def fetch_weather(
        self, latitude: float, longitude: float, days: int = 7
    ) -> Optional[Dict]:
        """
        Fetch forecast weather from Open-Meteo.
        Returns parsed JSON dict or None on network failure.
        """
        try:
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min,soil_moisture_0_to_7cm_mean",
                "forecast_days": min(max(days, 1), 16),
                "timezone": "Asia/Kolkata",
            }
            async with httpx.AsyncClient(timeout=float(self.timeout)) as client:
                resp = await client.get(self.base_url, params=params)
                resp.raise_for_status()
                data = resp.json()
                logger.info(f"Open-Meteo live weather fetched successfully for ({latitude}, {longitude})")
                return data
        except Exception as e:
            logger.warning(f"Open-Meteo fetch failed for ({latitude}, {longitude}): {e}")
            return None


weather_service = WeatherService()
