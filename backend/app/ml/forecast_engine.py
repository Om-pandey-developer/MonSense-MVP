"""
MonSense ML Forecast Engine
LSTM time-series + XGBoost downscaling ensemble for block-level rainfall prediction.
— Rohan Verma (Senior ML & Deep Learning Architect)
— Dr. Aarav Sharma (Chief Climatologist)

Architecture:
  1. LSTM captures temporal dependencies in rainfall sequences + teleconnection signals
  2. XGBoost downscales coarse grid predictions to block/village level using
     topographic features (elevation, aspect, land use)
  3. Ensemble combines both for final probabilistic forecast
"""

import numpy as np
from datetime import date, timedelta
from typing import List, Dict, Optional, Tuple
import logging
import hashlib
import json

logger = logging.getLogger(__name__)


class ClimateIndices:
    """Simulated teleconnection indices for demo.
    In production, these would be fetched from NOAA/BOM/IMD APIs."""

    @staticmethod
    def _date_rng(target_date: date, salt: str = "") -> np.random.RandomState:
        seed = int(hashlib.md5(f"{salt}_{target_date.isoformat()}".encode()).hexdigest()[:8], 16)
        return np.random.RandomState(seed)

    @classmethod
    def get_enso_nino34(cls, target_date: date) -> Tuple[float, str]:
        """Get ENSO Niño 3.4 SST anomaly."""
        # Simulate seasonal ENSO cycle
        day_of_year = target_date.timetuple().tm_yday
        rng = cls._date_rng(target_date, "enso")
        anomaly = 0.5 * np.sin(2 * np.pi * day_of_year / 365) + rng.normal(0, 0.3)
        if anomaly > 0.5:
            phase = "El Niño"
        elif anomaly < -0.5:
            phase = "La Niña"
        else:
            phase = "Neutral"
        return round(float(anomaly), 2), phase

    @classmethod
    def get_iod_dmi(cls, target_date: date) -> Tuple[float, str]:
        """Get Indian Ocean Dipole Mode Index."""
        day_of_year = target_date.timetuple().tm_yday
        rng = cls._date_rng(target_date, "iod")
        dmi = 0.3 * np.sin(2 * np.pi * (day_of_year - 90) / 365) + rng.normal(0, 0.2)
        if dmi > 0.4:
            phase = "Positive"
        elif dmi < -0.4:
            phase = "Negative"
        else:
            phase = "Neutral"
        return round(float(dmi), 2), phase

    @classmethod
    def get_mjo(cls, target_date: date) -> Tuple[int, float]:
        """Get MJO phase and amplitude (RMM index)."""
        day_of_year = target_date.timetuple().tm_yday
        rng = cls._date_rng(target_date, "mjo")
        phase = ((day_of_year // 5) % 8) + 1
        amplitude = abs(rng.normal(1.2, 0.5))
        return int(phase), round(float(amplitude), 2)


class MockDataGenerator:
    """Generates realistic-looking monsoon forecast data for MVP demo.
    Uses deterministic seeding based on location + date for consistency."""

    # Indian monsoon climatology (monthly avg rainfall mm/day for central India)
    MONTHLY_CLIMATOLOGY = {
        1: 2.0, 2: 3.0, 3: 5.0, 4: 8.0, 5: 15.0, 6: 45.0,
        7: 65.0, 8: 55.0, 9: 40.0, 10: 20.0, 11: 8.0, 12: 3.0
    }

    # State-level rainfall multipliers
    STATE_MULTIPLIERS = {
        "Maharashtra": 1.0, "Karnataka": 0.9, "Kerala": 1.4,
        "Tamil Nadu": 0.7, "Andhra Pradesh": 0.8, "Telangana": 0.85,
        "Madhya Pradesh": 0.95, "Rajasthan": 0.4, "Gujarat": 0.7,
        "Uttar Pradesh": 0.9, "Bihar": 1.1, "West Bengal": 1.3,
        "Odisha": 1.2, "Assam": 1.5, "Meghalaya": 1.8,
    }

    @classmethod
    def _get_seed(cls, location_code: str, target_date: date) -> int:
        """Deterministic seed for reproducible demo data."""
        key = f"{location_code}_{target_date.isoformat()}"
        return int(hashlib.md5(key.encode()).hexdigest()[:8], 16)

    @classmethod
    def generate_rainfall_prediction(
        cls,
        location_code: str,
        state_name: str,
        latitude: float,
        longitude: float,
        elevation_m: float,
        target_date: date,
        lead_days: int,
    ) -> Dict:
        """Generate a realistic rainfall prediction for a location and date."""
        seed = cls._get_seed(location_code, target_date)
        rng = np.random.RandomState(seed)

        # Base climatological rainfall
        month = target_date.month
        base_rainfall = cls.MONTHLY_CLIMATOLOGY.get(month, 10.0)

        # State multiplier
        state_mult = cls.STATE_MULTIPLIERS.get(state_name, 1.0)

        # Elevation effect (orographic enhancement)
        elev_mult = 1.0 + (elevation_m / 2000.0) * 0.5 if elevation_m else 1.0

        # Lead time degradation (skill decreases with longer lead)
        lead_factor = max(0.5, 1.0 - (lead_days / 60.0))

        # Climate index modulation
        enso_val, enso_phase = ClimateIndices.get_enso_nino34(target_date)
        iod_val, iod_phase = ClimateIndices.get_iod_dmi(target_date)
        mjo_phase, mjo_amp = ClimateIndices.get_mjo(target_date)

        # ENSO effect on Indian monsoon (El Niño → deficit, La Niña → excess)
        enso_effect = 1.0 - 0.15 * enso_val

        # IOD effect (Positive IOD → enhanced rainfall)
        iod_effect = 1.0 + 0.1 * iod_val

        # Compute predicted rainfall
        predicted = (
            base_rainfall * state_mult * elev_mult * lead_factor
            * enso_effect * iod_effect
            + rng.normal(0, base_rainfall * 0.2)
        )
        predicted = max(0, predicted)

        # Confidence interval
        uncertainty = predicted * (0.1 + lead_days * 0.015)
        lower = max(0, predicted - uncertainty)
        upper = predicted + uncertainty
        confidence = max(0.3, min(0.95, 0.9 - lead_days * 0.02))

        # Risk probabilities
        heavy_threshold = base_rainfall * 2.0
        heavy_prob = min(100, max(0, (predicted / heavy_threshold) * 60 + rng.normal(0, 10)))
        dry_prob = min(100, max(0, 100 - (predicted / base_rainfall) * 80 + rng.normal(0, 8)))

        # Monsoon onset probability (peaks in June for most of India)
        monsoon_onset_prob = 0.0
        if 5 <= month <= 7:
            onset_day = 152 + int(latitude * 0.8)  # Rough south-to-north progression
            days_diff = abs(target_date.timetuple().tm_yday - onset_day)
            monsoon_onset_prob = max(0, min(100, 90 - days_diff * 3))

        # Flood risk (high rainfall + flat terrain)
        flood_prob = min(100, max(0, heavy_prob * 0.7 + (1.0 - min(elevation_m or 100, 500) / 500) * 20))

        # Risk category
        max_prob = max(heavy_prob, flood_prob)
        if max_prob >= 70:
            risk = "very_high"
        elif max_prob >= 50:
            risk = "high"
        elif max_prob >= 30:
            risk = "moderate"
        elif max_prob >= 10:
            risk = "low"
        else:
            risk = "very_low"

        return {
            "predicted_rainfall_mm": round(predicted, 1),
            "rainfall_lower_bound": round(lower, 1),
            "rainfall_upper_bound": round(upper, 1),
            "prediction_confidence": round(confidence, 3),
            "heavy_rainfall_prob": round(heavy_prob, 1),
            "dry_spell_prob": round(dry_prob, 1),
            "monsoon_onset_prob": round(monsoon_onset_prob, 1),
            "flood_risk_prob": round(flood_prob, 1),
            "risk_category": risk,
            "model_version": "1.0.0-demo",
            "model_type": "LSTM+XGBoost Ensemble",
            "enso_value": enso_val,
            "enso_phase": enso_phase,
            "iod_value": iod_val,
            "iod_phase": iod_phase,
            "mjo_phase": mjo_phase,
            "mjo_amplitude": mjo_amp,
            "feature_importance": {
                "recent_rainfall": 0.28,
                "enso_nino34": 0.18,
                "iod_dmi": 0.12,
                "mjo_phase": 0.09,
                "elevation": 0.11,
                "latitude": 0.08,
                "day_of_year": 0.07,
                "soil_moisture": 0.07,
            },
        }

    @classmethod
    def generate_time_series(
        cls,
        location_code: str,
        state_name: str,
        latitude: float,
        longitude: float,
        elevation_m: float,
        start_date: date,
        days: int = 30,
    ) -> List[Dict]:
        """Generate a time-series forecast for the next N days."""
        forecasts = []
        for i in range(days):
            target = start_date + timedelta(days=i)
            prediction = cls.generate_rainfall_prediction(
                location_code, state_name, latitude, longitude,
                elevation_m, target, lead_days=i + 1,
            )
            prediction["target_date"] = target.isoformat()
            prediction["lead_days"] = i + 1
            forecasts.append(prediction)
        return forecasts


class ForecastEngine:
    """Main forecast engine that orchestrates LSTM + XGBoost pipeline.
    In production, this would load actual trained models.
    For MVP demo, uses MockDataGenerator with climatologically realistic outputs."""

    def __init__(self):
        self.model_loaded = False
        self.climate_indices = ClimateIndices()
        logger.info("ForecastEngine initialized (demo mode)")

    async def predict(
        self,
        location_code: str,
        state_name: str,
        latitude: float,
        longitude: float,
        elevation_m: float,
        target_date: date,
        lead_days: int = 7,
    ) -> Dict:
        """Run prediction for a single location and target date."""
        return MockDataGenerator.generate_rainfall_prediction(
            location_code, state_name, latitude, longitude,
            elevation_m, target_date, lead_days
        )

    async def predict_batch(
        self,
        locations: List[Dict],
        target_date: date,
    ) -> List[Dict]:
        """Run predictions for multiple locations (for risk map generation)."""
        results = []
        for loc in locations:
            lead_days = (target_date - date.today()).days
            lead_days = max(1, lead_days)
            prediction = MockDataGenerator.generate_rainfall_prediction(
                loc["code"], loc.get("state_name", "Maharashtra"),
                loc.get("latitude", 19.0), loc.get("longitude", 73.0),
                loc.get("elevation_m", 100), target_date, lead_days
            )
            prediction["location_id"] = loc["id"]
            prediction["location_code"] = loc["code"]
            prediction["location_name"] = loc["name"]
            prediction["target_date"] = target_date.isoformat()
            results.append(prediction)
        return results

    async def get_time_series(
        self,
        location_code: str,
        state_name: str,
        latitude: float,
        longitude: float,
        elevation_m: float,
        days: int = 30,
    ) -> List[Dict]:
        """Generate multi-day forecast time series."""
        return MockDataGenerator.generate_time_series(
            location_code, state_name, latitude, longitude,
            elevation_m, date.today(), days
        )


# Singleton
forecast_engine = ForecastEngine()
