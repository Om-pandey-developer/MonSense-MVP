"""
MonSense Crop Advisory Rule Engine
Generates crop-specific advisories based on forecast risk levels.
— Dr. Meenakshi Iyer (Agricultural Scientist & Agronomy Expert)
— Kabir Mehra (LLM & Prompt Engineering Integrator)

Rules are based on:
  - IMD thresholds for heavy/very heavy rainfall
  - Crop phenology stages and water requirements
  - ENSO/IOD-driven seasonal outlook
"""

from datetime import date
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


# ─── Crop Database ──────────────────────────────────────────────────────

CROP_DATABASE = {
    "rice": {
        "name_hi": "धान",
        "water_need_mm": {"sowing": 200, "vegetative": 300, "flowering": 250, "maturity": 150},
        "optimal_rainfall_mm": 1200,
        "drought_tolerance": "low",
        "waterlog_tolerance": "medium",
        "sowing_months": [6, 7],
    },
    "wheat": {
        "name_hi": "गेहूँ",
        "water_need_mm": {"sowing": 50, "vegetative": 150, "flowering": 100, "maturity": 75},
        "optimal_rainfall_mm": 400,
        "drought_tolerance": "medium",
        "waterlog_tolerance": "low",
        "sowing_months": [10, 11],
    },
    "cotton": {
        "name_hi": "कपास",
        "water_need_mm": {"sowing": 100, "vegetative": 200, "flowering": 180, "maturity": 120},
        "optimal_rainfall_mm": 700,
        "drought_tolerance": "medium",
        "waterlog_tolerance": "low",
        "sowing_months": [5, 6],
    },
    "soybean": {
        "name_hi": "सोयाबीन",
        "water_need_mm": {"sowing": 80, "vegetative": 180, "flowering": 150, "maturity": 100},
        "optimal_rainfall_mm": 600,
        "drought_tolerance": "medium",
        "waterlog_tolerance": "low",
        "sowing_months": [6, 7],
    },
    "groundnut": {
        "name_hi": "मूंगफली",
        "water_need_mm": {"sowing": 60, "vegetative": 150, "flowering": 120, "maturity": 80},
        "optimal_rainfall_mm": 500,
        "drought_tolerance": "high",
        "waterlog_tolerance": "low",
        "sowing_months": [6, 7],
    },
    "sugarcane": {
        "name_hi": "गन्ना",
        "water_need_mm": {"sowing": 150, "vegetative": 400, "flowering": 300, "maturity": 200},
        "optimal_rainfall_mm": 1500,
        "drought_tolerance": "low",
        "waterlog_tolerance": "medium",
        "sowing_months": [2, 3, 10],
    },
    "maize": {
        "name_hi": "मक्का",
        "water_need_mm": {"sowing": 60, "vegetative": 180, "flowering": 150, "maturity": 80},
        "optimal_rainfall_mm": 500,
        "drought_tolerance": "medium",
        "waterlog_tolerance": "low",
        "sowing_months": [6, 7],
    },
    "pulses": {
        "name_hi": "दालें",
        "water_need_mm": {"sowing": 40, "vegetative": 100, "flowering": 80, "maturity": 50},
        "optimal_rainfall_mm": 350,
        "drought_tolerance": "high",
        "waterlog_tolerance": "low",
        "sowing_months": [6, 7, 10],
    },
}


# ─── Advisory Templates ─────────────────────────────────────────────────

ADVISORY_TEMPLATES = {
    "delay_sowing": {
        "en": "⏳ DELAY SOWING: Heavy rainfall ({rainfall_mm}mm) expected in next {lead_days} days. Wait for stable weather before sowing {crop_name}. Risk of seed rot and waterlogging.",
        "hi": "⏳ बुवाई में देरी करें: अगले {lead_days} दिनों में भारी बारिश ({rainfall_mm}mm) की संभावना। {crop_name_hi} की बुवाई के लिए मौसम स्थिर होने तक प्रतीक्षा करें। बीज सड़ने और जलभराव का खतरा।",
    },
    "proceed_sowing": {
        "en": "✅ GOOD TO SOW: Favorable conditions for {crop_name} sowing in next {lead_days} days. Expected rainfall: {rainfall_mm}mm. Adequate soil moisture anticipated.",
        "hi": "✅ बुवाई के लिए उपयुक्त: अगले {lead_days} दिनों में {crop_name_hi} की बुवाई के लिए अनुकूल परिस्थितियाँ। अपेक्षित वर्षा: {rainfall_mm}mm। पर्याप्त मिट्टी नमी की संभावना।",
    },
    "arrange_irrigation": {
        "en": "💧 ARRANGE IRRIGATION: Dry spell expected. Only {rainfall_mm}mm rain forecast for next {lead_days} days. {crop_name} at {crop_stage} stage needs {water_need}mm. Arrange supplemental irrigation.",
        "hi": "💧 सिंचाई की व्यवस्था करें: सूखे का अनुमान। अगले {lead_days} दिनों में केवल {rainfall_mm}mm बारिश का पूर्वानुमान। {crop_name_hi} {crop_stage} अवस्था में {water_need}mm पानी की आवश्यकता। अतिरिक्त सिंचाई की व्यवस्था करें।",
    },
    "drain_fields": {
        "en": "🚿 DRAIN FIELDS: Very heavy rainfall ({rainfall_mm}mm) expected. Ensure proper drainage for {crop_name}. Risk of waterlogging and root damage.",
        "hi": "🚿 खेत से पानी निकालें: बहुत भारी बारिश ({rainfall_mm}mm) का अनुमान। {crop_name_hi} के लिए उचित जल निकासी सुनिश्चित करें। जलभराव और जड़ क्षति का खतरा।",
    },
    "harvest_early": {
        "en": "🌾 HARVEST EARLY: Heavy rain ({rainfall_mm}mm) forecast in {lead_days} days. If {crop_name} is near maturity, consider early harvest to prevent crop damage.",
        "hi": "🌾 जल्दी कटाई करें: {lead_days} दिनों में भारी बारिश ({rainfall_mm}mm) का पूर्वानुमान। यदि {crop_name_hi} परिपक्वता के करीब है, तो फसल क्षति से बचने के लिए जल्दी कटाई पर विचार करें।",
    },
    "apply_fungicide": {
        "en": "🧪 APPLY FUNGICIDE: Prolonged wet conditions expected. {crop_name} at {crop_stage} stage is vulnerable to fungal diseases. Apply preventive fungicide spray.",
        "hi": "🧪 कवकनाशी छिड़काव करें: लंबे समय तक गीली परिस्थितियों का अनुमान। {crop_name_hi} {crop_stage} अवस्था में फंगल रोगों के प्रति संवेदनशील। निवारक कवकनाशी छिड़काव करें।",
    },
    "monsoon_onset_alert": {
        "en": "🌧️ MONSOON ONSET ALERT: {monsoon_prob}% probability of monsoon onset in your area within {lead_days} days. Prepare fields for {crop_name} sowing.",
        "hi": "🌧️ मानसून आगमन सूचना: अगले {lead_days} दिनों में आपके क्षेत्र में मानसून आगमन की {monsoon_prob}% संभावना। {crop_name_hi} की बुवाई के लिए खेत तैयार करें।",
    },
    "flood_warning": {
        "en": "⚠️ FLOOD WARNING: {flood_prob}% flood risk in your area. Expected rainfall: {rainfall_mm}mm in {lead_days} days. Move livestock and stored grain to higher ground. Stay alert.",
        "hi": "⚠️ बाढ़ चेतावनी: आपके क्षेत्र में {flood_prob}% बाढ़ का खतरा। {lead_days} दिनों में अपेक्षित वर्षा: {rainfall_mm}mm। पशुधन और भंडारित अनाज को ऊँचे स्थान पर ले जाएँ। सतर्क रहें।",
    },
}


class CropAdvisoryEngine:
    """Rule-based advisory engine that converts forecast data into actionable
    crop-specific advisories for farmers."""

    def __init__(self):
        self.crop_db = CROP_DATABASE
        self.templates = ADVISORY_TEMPLATES

    def _get_crop_stage(self, crop_name: str, current_date: date) -> str:
        """Determine current crop growth stage based on sowing calendar."""
        crop = self.crop_db.get(crop_name)
        if not crop:
            return "vegetative"

        month = current_date.month
        sowing_months = crop["sowing_months"]

        # Estimate stage based on months since sowing
        for sm in sowing_months:
            months_since = (month - sm) % 12
            if months_since <= 1:
                return "sowing"
            elif months_since <= 3:
                return "vegetative"
            elif months_since <= 4:
                return "flowering"
            elif months_since <= 5:
                return "maturity"
            elif months_since <= 6:
                return "harvest"
        return "pre_sowing"

    def generate_advisory(
        self,
        crop_name: str,
        forecast: Dict,
        current_date: Optional[date] = None,
        crop_stage: Optional[str] = None,
    ) -> List[Dict]:
        """Generate advisories for a single crop based on forecast data."""
        if current_date is None:
            current_date = date.today()

        crop = self.crop_db.get(crop_name, self.crop_db.get("rice"))
        if not crop_stage:
            crop_stage = self._get_crop_stage(crop_name, current_date)
        advisories = []

        rainfall = forecast.get("predicted_rainfall_mm", 0)
        heavy_prob = forecast.get("heavy_rainfall_prob", 0)
        dry_prob = forecast.get("dry_spell_prob", 0)
        monsoon_prob = forecast.get("monsoon_onset_prob", 0)
        flood_prob = forecast.get("flood_risk_prob", 0)
        lead_days = forecast.get("lead_days", 7)
        risk = forecast.get("risk_category", "low")

        crop_name_hi = crop.get("name_hi", crop_name)
        water_need = crop["water_need_mm"].get(crop_stage, 100)

        template_vars = {
            "crop_name": crop_name.title(),
            "crop_name_hi": crop_name_hi,
            "crop_stage": crop_stage,
            "rainfall_mm": rainfall,
            "lead_days": lead_days,
            "water_need": water_need,
            "heavy_prob": heavy_prob,
            "dry_prob": dry_prob,
            "monsoon_prob": monsoon_prob,
            "flood_prob": flood_prob,
        }

        # Rule 1: Monsoon onset alert
        if monsoon_prob > 50 and crop_stage == "pre_sowing":
            advisories.append(self._create_advisory(
                "monsoon_onset_alert", "info", crop_name, crop_stage, template_vars
            ))

        # Rule 2: Delay sowing if heavy rain during sowing period
        if crop_stage == "sowing" and heavy_prob > 60:
            advisories.append(self._create_advisory(
                "delay_sowing", "warning", crop_name, crop_stage, template_vars
            ))

        # Rule 3: Good sowing conditions
        elif crop_stage in ("sowing", "pre_sowing") and 10 < rainfall < 50 and heavy_prob < 30:
            advisories.append(self._create_advisory(
                "proceed_sowing", "info", crop_name, crop_stage, template_vars
            ))

        # Rule 4: Arrange irrigation for dry spell
        if dry_prob > 60 and crop_stage in ("vegetative", "flowering"):
            advisories.append(self._create_advisory(
                "arrange_irrigation", "warning", crop_name, crop_stage, template_vars
            ))

        # Rule 5: Drain fields for waterlog-sensitive crops
        if heavy_prob > 70 and crop.get("waterlog_tolerance") == "low":
            advisories.append(self._create_advisory(
                "drain_fields", "warning", crop_name, crop_stage, template_vars
            ))

        # Rule 6: Early harvest alert
        if crop_stage == "maturity" and heavy_prob > 50:
            advisories.append(self._create_advisory(
                "harvest_early", "critical", crop_name, crop_stage, template_vars
            ))

        # Rule 7: Fungicide advisory for prolonged wet conditions
        if rainfall > 30 and heavy_prob > 40 and crop_stage in ("vegetative", "flowering"):
            advisories.append(self._create_advisory(
                "apply_fungicide", "info", crop_name, crop_stage, template_vars
            ))

        # Rule 8: Flood warning
        if flood_prob > 60:
            advisories.append(self._create_advisory(
                "flood_warning", "critical", crop_name, crop_stage, template_vars
            ))

        return advisories

    def _create_advisory(
        self,
        advisory_type: str,
        severity: str,
        crop_name: str,
        crop_stage: str,
        template_vars: Dict,
    ) -> Dict:
        """Create a structured advisory dict from a template."""
        template = self.templates.get(advisory_type, {})
        text_en = template.get("en", "").format(**template_vars)
        text_hi = template.get("hi", "").format(**template_vars)

        return {
            "crop_name": crop_name,
            "crop_stage": crop_stage,
            "advisory_type": advisory_type,
            "advisory_text_en": text_en,
            "advisory_text_hi": text_hi,
            "severity": severity,
            "actions": self._get_actions(advisory_type),
        }

    def _get_actions(self, advisory_type: str) -> Dict:
        """Get structured action items for an advisory type."""
        actions_map = {
            "delay_sowing": {
                "primary": "Wait 3-5 days before sowing",
                "secondary": "Monitor weather updates",
                "preparation": "Keep seeds ready, prepare nursery under cover",
            },
            "proceed_sowing": {
                "primary": "Proceed with sowing in next 2-3 days",
                "secondary": "Apply pre-sowing fertilizer",
                "preparation": "Ensure seed treatment is done",
            },
            "arrange_irrigation": {
                "primary": "Arrange supplemental irrigation",
                "secondary": "Apply mulch to retain soil moisture",
                "preparation": "Check irrigation pump and channels",
            },
            "drain_fields": {
                "primary": "Create drainage channels",
                "secondary": "Raise bunds around low-lying areas",
                "preparation": "Clear existing drainage routes",
            },
            "harvest_early": {
                "primary": "Begin harvest immediately if crop is ready",
                "secondary": "Arrange storage and transport",
                "preparation": "Prepare threshing floor under cover",
            },
            "apply_fungicide": {
                "primary": "Apply recommended fungicide spray",
                "secondary": "Ensure proper spacing for air circulation",
                "preparation": "Procure fungicide from nearest agri-center",
            },
            "monsoon_onset_alert": {
                "primary": "Prepare fields — ploughing and leveling",
                "secondary": "Procure seeds and fertilizer",
                "preparation": "Plan sowing schedule based on forecast",
            },
            "flood_warning": {
                "primary": "Move livestock and grain to safety",
                "secondary": "Reinforce bunds and embankments",
                "preparation": "Keep emergency supplies ready",
            },
        }
        return actions_map.get(advisory_type, {})

    def generate_multi_crop_advisory(
        self,
        crop_names: List[str],
        forecast: Dict,
    ) -> List[Dict]:
        """Generate advisories for multiple crops at a location."""
        all_advisories = []
        for crop in crop_names:
            advisories = self.generate_advisory(crop, forecast)
            all_advisories.extend(advisories)
        return all_advisories

    def simulate_from_params(
        self,
        rainfall_mm: float,
        dry_spell_days: int = 0,
        crop: str = "rice",
        crop_stage: str = "flowering",
        heavy_rainfall_prob: float = 0.0,
        flood_risk_prob: float = 0.0,
        lead_days: int = 7,
    ) -> List[Dict]:
        """Simulate dynamic advisories from user-controlled agronomic parameters."""
        r = float(rainfall_mm)
        d = int(dry_spell_days)
        heavy_p = float(heavy_rainfall_prob or (80.0 if r >= 65 else 45.0 if r >= 35 else 10.0))
        dry_p = float(min(100.0, d * 14.0) if d > 0 else 5.0)
        flood_p = float(flood_risk_prob or (70.0 if r >= 70 else 35.0 if r >= 45 else 10.0))

        risk_category = "very_high" if r >= 70 or d >= 10 else "high" if r >= 50 or d >= 6 else "moderate" if r >= 30 or d >= 3 else "low"

        forecast = {
            "predicted_rainfall_mm": r,
            "lead_days": lead_days,
            "target_date": date.today().isoformat(),
            "heavy_rainfall_prob": heavy_p,
            "dry_spell_prob": dry_p,
            "monsoon_onset_prob": 50.0 if crop_stage == "pre_sowing" else 0.0,
            "flood_risk_prob": flood_p,
            "risk_category": risk_category,
        }
        return self.generate_advisory(crop_name=crop, forecast=forecast, crop_stage=crop_stage)


# Singleton
advisory_engine = CropAdvisoryEngine()

