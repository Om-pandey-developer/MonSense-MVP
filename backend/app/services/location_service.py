"""
MonSense Location Service
Provides seed data and location management for the demo.
— Priya Nair (Data Engineering & Spatial Pipeline Lead)
"""

from datetime import date
from typing import List, Dict, Optional
from uuid import UUID, uuid4


# ─── Demo Location Data ─────────────────────────────────────────────────
# Maharashtra state with districts, blocks, and villages for MVP demo

DEMO_LOCATIONS = [
    # State
    {
        "id": "a0000001-0000-0000-0000-000000000001",
        "name": "Maharashtra",
        "name_local": "महाराष्ट्र",
        "code": "MH",
        "level": "state",
        "parent_id": None,
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 19.7515,
        "longitude": 75.7139,
        "elevation_m": 500,
        "area_sq_km": 307713,
    },
    # Districts
    {
        "id": "b0000001-0000-0000-0000-000000000001",
        "name": "Pune",
        "name_local": "पुणे",
        "code": "MH-PUN",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "elevation_m": 560,
        "area_sq_km": 15643,
    },
    {
        "id": "b0000002-0000-0000-0000-000000000001",
        "name": "Nagpur",
        "name_local": "नागपूर",
        "code": "MH-NAG",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Nagpur",
        "latitude": 21.1458,
        "longitude": 79.0882,
        "elevation_m": 310,
        "area_sq_km": 9892,
    },
    {
        "id": "b0000003-0000-0000-0000-000000000001",
        "name": "Nashik",
        "name_local": "नाशिक",
        "code": "MH-NAS",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Nashik",
        "latitude": 20.0,
        "longitude": 73.78,
        "elevation_m": 700,
        "area_sq_km": 15530,
    },
    {
        "id": "b0000004-0000-0000-0000-000000000001",
        "name": "Aurangabad",
        "name_local": "औरंगाबाद",
        "code": "MH-AUR",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Aurangabad",
        "latitude": 19.8762,
        "longitude": 75.3433,
        "elevation_m": 570,
        "area_sq_km": 10100,
    },
    {
        "id": "b0000005-0000-0000-0000-000000000001",
        "name": "Kolhapur",
        "name_local": "कोल्हापूर",
        "code": "MH-KOL",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Kolhapur",
        "latitude": 16.7050,
        "longitude": 74.2433,
        "elevation_m": 569,
        "area_sq_km": 7685,
    },
    {
        "id": "b0000006-0000-0000-0000-000000000001",
        "name": "Solapur",
        "name_local": "सोलापूर",
        "code": "MH-SOL",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Solapur",
        "latitude": 17.6599,
        "longitude": 75.9064,
        "elevation_m": 458,
        "area_sq_km": 14895,
    },
    {
        "id": "b0000007-0000-0000-0000-000000000001",
        "name": "Satara",
        "name_local": "सातारा",
        "code": "MH-SAT",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Satara",
        "latitude": 17.6805,
        "longitude": 74.0183,
        "elevation_m": 750,
        "area_sq_km": 10480,
    },
    {
        "id": "b0000008-0000-0000-0000-000000000001",
        "name": "Ahmednagar",
        "name_local": "अहमदनगर",
        "code": "MH-AHM",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Ahmednagar",
        "latitude": 19.0948,
        "longitude": 74.7480,
        "elevation_m": 649,
        "area_sq_km": 17048,
    },
    # Blocks (under Pune district)
    {
        "id": "c0000001-0000-0000-0000-000000000001",
        "name": "Baramati",
        "name_local": "बारामती",
        "code": "MH-PUN-BAR",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.1514,
        "longitude": 74.5777,
        "elevation_m": 550,
        "area_sq_km": 1380,
    },
    {
        "id": "c0000002-0000-0000-0000-000000000001",
        "name": "Indapur",
        "name_local": "इंदापूर",
        "code": "MH-PUN-IND",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.1130,
        "longitude": 75.0237,
        "elevation_m": 500,
        "area_sq_km": 1520,
    },
    {
        "id": "c0000003-0000-0000-0000-000000000001",
        "name": "Junnar",
        "name_local": "जुन्नर",
        "code": "MH-PUN-JUN",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 19.2079,
        "longitude": 73.8749,
        "elevation_m": 720,
        "area_sq_km": 1610,
    },
    {
        "id": "c0000004-0000-0000-0000-000000000001",
        "name": "Haveli",
        "name_local": "हवेली",
        "code": "MH-PUN-HAV",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.5000,
        "longitude": 73.8500,
        "elevation_m": 580,
        "area_sq_km": 930,
    },
    {
        "id": "c0000005-0000-0000-0000-000000000001",
        "name": "Mulshi",
        "name_local": "मुळशी",
        "code": "MH-PUN-MUL",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.5300,
        "longitude": 73.5100,
        "elevation_m": 900,
        "area_sq_km": 1070,
    },
    {
        "id": "c0000006-0000-0000-0000-000000000001",
        "name": "Shirur",
        "name_local": "शिरूर",
        "code": "MH-PUN-SHR",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.8300,
        "longitude": 74.3700,
        "elevation_m": 510,
        "area_sq_km": 1440,
    },
    # Blocks (under Nagpur)
    {
        "id": "c0000007-0000-0000-0000-000000000001",
        "name": "Nagpur Rural",
        "name_local": "नागपूर ग्रामीण",
        "code": "MH-NAG-RUR",
        "level": "block",
        "parent_id": "b0000002-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Nagpur",
        "latitude": 21.1500,
        "longitude": 79.0500,
        "elevation_m": 310,
        "area_sq_km": 1250,
    },
    {
        "id": "c0000008-0000-0000-0000-000000000001",
        "name": "Kamptee",
        "name_local": "कामठी",
        "code": "MH-NAG-KAM",
        "level": "block",
        "parent_id": "b0000002-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Nagpur",
        "latitude": 21.2300,
        "longitude": 79.2000,
        "elevation_m": 290,
        "area_sq_km": 1180,
    },
    # Blocks (under Nashik)
    {
        "id": "c0000009-0000-0000-0000-000000000001",
        "name": "Igatpuri",
        "name_local": "इगतपुरी",
        "code": "MH-NAS-IGT",
        "level": "block",
        "parent_id": "b0000003-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Nashik",
        "latitude": 19.6900,
        "longitude": 73.5600,
        "elevation_m": 900,
        "area_sq_km": 1350,
    },
    {
        "id": "c0000010-0000-0000-0000-000000000001",
        "name": "Malegaon",
        "name_local": "मालेगाव",
        "code": "MH-NAS-MAL",
        "level": "block",
        "parent_id": "b0000003-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Nashik",
        "latitude": 20.5500,
        "longitude": 74.5300,
        "elevation_m": 480,
        "area_sq_km": 1690,
    },
    # Villages (under Baramati block)
    {
        "id": "d0000001-0000-0000-0000-000000000001",
        "name": "Malad",
        "name_local": "मालाड",
        "code": "MH-PUN-BAR-MAL",
        "level": "village",
        "parent_id": "c0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.1600,
        "longitude": 74.5900,
        "elevation_m": 540,
        "area_sq_km": 12,
    },
    {
        "id": "d0000002-0000-0000-0000-000000000001",
        "name": "Supe",
        "name_local": "सुपे",
        "code": "MH-PUN-BAR-SUP",
        "level": "village",
        "parent_id": "c0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.1200,
        "longitude": 74.5400,
        "elevation_m": 535,
        "area_sq_km": 8,
    },
    {
        "id": "d0000003-0000-0000-0000-000000000001",
        "name": "Katewadi",
        "name_local": "काटेवाडी",
        "code": "MH-PUN-BAR-KAT",
        "level": "village",
        "parent_id": "c0000001-0000-0000-0000-000000000001",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.1800,
        "longitude": 74.6200,
        "elevation_m": 545,
        "area_sq_km": 6,
    },
]


class LocationService:
    """In-memory location service for MVP demo.
    In production, this would query PostGIS database."""

    def __init__(self):
        self.locations = {loc["id"]: loc for loc in DEMO_LOCATIONS}

    def get_all(self, level: Optional[str] = None) -> List[Dict]:
        """Get all locations, optionally filtered by level."""
        locs = list(self.locations.values())
        if level:
            locs = [l for l in locs if l["level"] == level]
        return locs

    def get_by_id(self, location_id: str) -> Optional[Dict]:
        """Get location by ID."""
        return self.locations.get(location_id)

    def get_by_code(self, code: str) -> Optional[Dict]:
        """Get location by code."""
        for loc in self.locations.values():
            if loc["code"] == code:
                return loc
        return None

    def get_children(self, parent_id: str) -> List[Dict]:
        """Get child locations of a parent."""
        return [l for l in self.locations.values() if l["parent_id"] == parent_id]

    def get_by_district(self, district_name: str) -> List[Dict]:
        """Get all locations in a district."""
        return [
            l for l in self.locations.values()
            if l.get("district_name") == district_name
        ]

    def get_blocks(self, district_id: Optional[str] = None) -> List[Dict]:
        """Get all blocks, optionally filtered by district."""
        blocks = [l for l in self.locations.values() if l["level"] == "block"]
        if district_id:
            blocks = [b for b in blocks if b["parent_id"] == district_id]
        return blocks

    def search(self, query: str) -> List[Dict]:
        """Search locations by name."""
        query_lower = query.lower()
        return [
            l for l in self.locations.values()
            if query_lower in l["name"].lower() or query_lower in (l.get("name_local") or "")
        ]


# Singleton
location_service = LocationService()
