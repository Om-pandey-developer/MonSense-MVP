"""
MonSense Location Service
Provides seed data and location management for Pan-India (All 30 States & UTs).
— Priya Nair (Data Engineering & Spatial Pipeline Lead)
"""

from datetime import date
from typing import List, Dict, Optional
from uuid import UUID, uuid4


# ─── Pan-India Location Data (30 States & UTs) ───────────────────────────
DEMO_LOCATIONS = [
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
        "area_sq_km": 307713
    },
    {
        "id": "a0000002-0000-0000-0000-000000000001",
        "name": "Karnataka",
        "name_local": "ಕರ್ನಾಟಕ",
        "code": "KA",
        "level": "state",
        "parent_id": None,
        "state_name": "Karnataka",
        "district_name": None,
        "latitude": 15.3173,
        "longitude": 75.7139,
        "elevation_m": 600,
        "area_sq_km": 191791
    },
    {
        "id": "a0000003-0000-0000-0000-000000000001",
        "name": "Gujarat",
        "name_local": "ગુજરાત",
        "code": "GJ",
        "level": "state",
        "parent_id": None,
        "state_name": "Gujarat",
        "district_name": None,
        "latitude": 22.2587,
        "longitude": 71.1924,
        "elevation_m": 120,
        "area_sq_km": 196024
    },
    {
        "id": "a0000004-0000-0000-0000-000000000001",
        "name": "Madhya Pradesh",
        "name_local": "मध्य प्रदेश",
        "code": "MP",
        "level": "state",
        "parent_id": None,
        "state_name": "Madhya Pradesh",
        "district_name": None,
        "latitude": 22.9734,
        "longitude": 78.6569,
        "elevation_m": 450,
        "area_sq_km": 308252
    },
    {
        "id": "a0000005-0000-0000-0000-000000000001",
        "name": "Punjab",
        "name_local": "ਪੰਜਾਬ",
        "code": "PB",
        "level": "state",
        "parent_id": None,
        "state_name": "Punjab",
        "district_name": None,
        "latitude": 31.1471,
        "longitude": 75.3412,
        "elevation_m": 250,
        "area_sq_km": 50362
    },
    {
        "id": "a0000006-0000-0000-0000-000000000001",
        "name": "Uttar Pradesh",
        "name_local": "उत्तर प्रदेश",
        "code": "UP",
        "level": "state",
        "parent_id": None,
        "state_name": "Uttar Pradesh",
        "district_name": None,
        "latitude": 26.8467,
        "longitude": 80.9462,
        "elevation_m": 125,
        "area_sq_km": 240928
    },
    {
        "id": "a0000007-0000-0000-0000-000000000001",
        "name": "Andhra Pradesh",
        "name_local": "ఆంధ్రప్రదేశ్",
        "code": "AP",
        "level": "state",
        "parent_id": None,
        "state_name": "Andhra Pradesh",
        "district_name": None,
        "latitude": 15.9129,
        "longitude": 79.74,
        "elevation_m": 150,
        "area_sq_km": 162968
    },
    {
        "id": "a0000008-0000-0000-0000-000000000001",
        "name": "Arunachal Pradesh",
        "name_local": "অৰুণাচল প্ৰদেশ",
        "code": "AR",
        "level": "state",
        "parent_id": None,
        "state_name": "Arunachal Pradesh",
        "district_name": None,
        "latitude": 28.218,
        "longitude": 94.7278,
        "elevation_m": 1200,
        "area_sq_km": 83743
    },
    {
        "id": "a0000009-0000-0000-0000-000000000001",
        "name": "Assam",
        "name_local": "অসম",
        "code": "AS",
        "level": "state",
        "parent_id": None,
        "state_name": "Assam",
        "district_name": None,
        "latitude": 26.2006,
        "longitude": 92.9376,
        "elevation_m": 100,
        "area_sq_km": 78438
    },
    {
        "id": "a0000010-0000-0000-0000-000000000001",
        "name": "Bihar",
        "name_local": "बिहार",
        "code": "BR",
        "level": "state",
        "parent_id": None,
        "state_name": "Bihar",
        "district_name": None,
        "latitude": 25.0961,
        "longitude": 85.3131,
        "elevation_m": 53,
        "area_sq_km": 94163
    },
    {
        "id": "a0000011-0000-0000-0000-000000000001",
        "name": "Chhattisgarh",
        "name_local": "छत्तीसगढ़",
        "code": "CG",
        "level": "state",
        "parent_id": None,
        "state_name": "Chhattisgarh",
        "district_name": None,
        "latitude": 21.2787,
        "longitude": 81.8661,
        "elevation_m": 298,
        "area_sq_km": 135192
    },
    {
        "id": "a0000012-0000-0000-0000-000000000001",
        "name": "Goa",
        "name_local": "गोंय",
        "code": "GA",
        "level": "state",
        "parent_id": None,
        "state_name": "Goa",
        "district_name": None,
        "latitude": 15.2993,
        "longitude": 74.124,
        "elevation_m": 10,
        "area_sq_km": 3702
    },
    {
        "id": "a0000013-0000-0000-0000-000000000001",
        "name": "Haryana",
        "name_local": "हरियाणा",
        "code": "HR",
        "level": "state",
        "parent_id": None,
        "state_name": "Haryana",
        "district_name": None,
        "latitude": 29.0588,
        "longitude": 76.0856,
        "elevation_m": 220,
        "area_sq_km": 44212
    },
    {
        "id": "a0000014-0000-0000-0000-000000000001",
        "name": "Himachal Pradesh",
        "name_local": "हिमाचल प्रदेश",
        "code": "HP",
        "level": "state",
        "parent_id": None,
        "state_name": "Himachal Pradesh",
        "district_name": None,
        "latitude": 31.1048,
        "longitude": 77.1734,
        "elevation_m": 2200,
        "area_sq_km": 55673
    },
    {
        "id": "a0000015-0000-0000-0000-000000000001",
        "name": "Jharkhand",
        "name_local": "झारखंड",
        "code": "JH",
        "level": "state",
        "parent_id": None,
        "state_name": "Jharkhand",
        "district_name": None,
        "latitude": 23.6102,
        "longitude": 85.2799,
        "elevation_m": 650,
        "area_sq_km": 79716
    },
    {
        "id": "a0000016-0000-0000-0000-000000000001",
        "name": "Kerala",
        "name_local": "കേരളം",
        "code": "KL",
        "level": "state",
        "parent_id": None,
        "state_name": "Kerala",
        "district_name": None,
        "latitude": 10.8505,
        "longitude": 76.2711,
        "elevation_m": 300,
        "area_sq_km": 38863
    },
    {
        "id": "a0000017-0000-0000-0000-000000000001",
        "name": "Manipur",
        "name_local": "মণিপুর",
        "code": "MN",
        "level": "state",
        "parent_id": None,
        "state_name": "Manipur",
        "district_name": None,
        "latitude": 24.6637,
        "longitude": 93.9063,
        "elevation_m": 780,
        "area_sq_km": 22327
    },
    {
        "id": "a0000018-0000-0000-0000-000000000001",
        "name": "Meghalaya",
        "name_local": "मेघालय",
        "code": "ML",
        "level": "state",
        "parent_id": None,
        "state_name": "Meghalaya",
        "district_name": None,
        "latitude": 25.467,
        "longitude": 91.3662,
        "elevation_m": 1496,
        "area_sq_km": 22429
    },
    {
        "id": "a0000019-0000-0000-0000-000000000001",
        "name": "Mizoram",
        "name_local": "मिज़ोरम",
        "code": "MZ",
        "level": "state",
        "parent_id": None,
        "state_name": "Mizoram",
        "district_name": None,
        "latitude": 23.1645,
        "longitude": 92.9376,
        "elevation_m": 1132,
        "area_sq_km": 21081
    },
    {
        "id": "a0000020-0000-0000-0000-000000000001",
        "name": "Nagaland",
        "name_local": "नागालैंड",
        "code": "NL",
        "level": "state",
        "parent_id": None,
        "state_name": "Nagaland",
        "district_name": None,
        "latitude": 26.1584,
        "longitude": 94.5624,
        "elevation_m": 1444,
        "area_sq_km": 16579
    },
    {
        "id": "a0000021-0000-0000-0000-000000000001",
        "name": "Odisha",
        "name_local": "ଓଡ଼ିଶା",
        "code": "OD",
        "level": "state",
        "parent_id": None,
        "state_name": "Odisha",
        "district_name": None,
        "latitude": 20.9517,
        "longitude": 85.9836,
        "elevation_m": 45,
        "area_sq_km": 155707
    },
    {
        "id": "a0000022-0000-0000-0000-000000000001",
        "name": "Rajasthan",
        "name_local": "राजस्थान",
        "code": "RJ",
        "level": "state",
        "parent_id": None,
        "state_name": "Rajasthan",
        "district_name": None,
        "latitude": 27.0238,
        "longitude": 74.2179,
        "elevation_m": 350,
        "area_sq_km": 342239
    },
    {
        "id": "a0000023-0000-0000-0000-000000000001",
        "name": "Sikkim",
        "name_local": "सिक्किम",
        "code": "SK",
        "level": "state",
        "parent_id": None,
        "state_name": "Sikkim",
        "district_name": None,
        "latitude": 27.533,
        "longitude": 88.5122,
        "elevation_m": 1650,
        "area_sq_km": 7096
    },
    {
        "id": "a0000024-0000-0000-0000-000000000001",
        "name": "Tamil Nadu",
        "name_local": "தமிழ்நாடு",
        "code": "TN",
        "level": "state",
        "parent_id": None,
        "state_name": "Tamil Nadu",
        "district_name": None,
        "latitude": 11.1271,
        "longitude": 78.6569,
        "elevation_m": 150,
        "area_sq_km": 130058
    },
    {
        "id": "a0000025-0000-0000-0000-000000000001",
        "name": "Telangana",
        "name_local": "తెలంగాణ",
        "code": "TS",
        "level": "state",
        "parent_id": None,
        "state_name": "Telangana",
        "district_name": None,
        "latitude": 18.1124,
        "longitude": 79.0193,
        "elevation_m": 480,
        "area_sq_km": 112077
    },
    {
        "id": "a0000026-0000-0000-0000-000000000001",
        "name": "Tripura",
        "name_local": "ত্রিপুরা",
        "code": "TR",
        "level": "state",
        "parent_id": None,
        "state_name": "Tripura",
        "district_name": None,
        "latitude": 23.9408,
        "longitude": 91.9882,
        "elevation_m": 45,
        "area_sq_km": 10491
    },
    {
        "id": "a0000027-0000-0000-0000-000000000001",
        "name": "Uttarakhand",
        "name_local": "उत्तराखण्ड",
        "code": "UK",
        "level": "state",
        "parent_id": None,
        "state_name": "Uttarakhand",
        "district_name": None,
        "latitude": 30.0668,
        "longitude": 79.0193,
        "elevation_m": 1500,
        "area_sq_km": 53483
    },
    {
        "id": "a0000028-0000-0000-0000-000000000001",
        "name": "West Bengal",
        "name_local": "पश्चिमবঙ্গ",
        "code": "WB",
        "level": "state",
        "parent_id": None,
        "state_name": "West Bengal",
        "district_name": None,
        "latitude": 22.9868,
        "longitude": 87.855,
        "elevation_m": 30,
        "area_sq_km": 88752
    },
    {
        "id": "a0000029-0000-0000-0000-000000000001",
        "name": "Delhi (NCT)",
        "name_local": "दिल्ली",
        "code": "DL",
        "level": "state",
        "parent_id": None,
        "state_name": "Delhi (NCT)",
        "district_name": None,
        "latitude": 28.7041,
        "longitude": 77.1025,
        "elevation_m": 216,
        "area_sq_km": 1484
    },
    {
        "id": "a0000030-0000-0000-0000-000000000001",
        "name": "Jammu & Kashmir",
        "name_local": "جموں و کشمیر",
        "code": "JK",
        "level": "state",
        "parent_id": None,
        "state_name": "Jammu & Kashmir",
        "district_name": None,
        "latitude": 33.7782,
        "longitude": 76.5762,
        "elevation_m": 1600,
        "area_sq_km": 42241
    },
    {
        "id": "b0000001-0000-0000-0000-000000000001",
        "name": "Pune",
        "name_local": "पुणे",
        "code": "MH-PUN",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 18.5204,
        "longitude": 73.8567,
        "elevation_m": 560,
        "area_sq_km": 38464
    },
    {
        "id": "c0000001-0000-0000-0000-000000000001",
        "name": "Baramati",
        "name_local": "Baramati",
        "code": "MH-PUN-BAR",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.1514,
        "longitude": 74.5777,
        "elevation_m": 550,
        "area_sq_km": 450
    },
    {
        "id": "c0000002-0000-0000-0000-000000000001",
        "name": "Indapur",
        "name_local": "Indapur",
        "code": "MH-PUN-IND",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.113,
        "longitude": 75.0237,
        "elevation_m": 500,
        "area_sq_km": 450
    },
    {
        "id": "c0000003-0000-0000-0000-000000000001",
        "name": "Junnar",
        "name_local": "Junnar",
        "code": "MH-PUN-JUN",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 19.2079,
        "longitude": 73.8749,
        "elevation_m": 720,
        "area_sq_km": 450
    },
    {
        "id": "c0000004-0000-0000-0000-000000000001",
        "name": "Haveli",
        "name_local": "Haveli",
        "code": "MH-PUN-HAV",
        "level": "block",
        "parent_id": "b0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Pune",
        "latitude": 18.5,
        "longitude": 73.85,
        "elevation_m": 580,
        "area_sq_km": 450
    },
    {
        "id": "b0000002-0000-0000-0000-000000000001",
        "name": "Nagpur",
        "name_local": "नागपूर",
        "code": "MH-NAG",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 21.1458,
        "longitude": 79.0882,
        "elevation_m": 310,
        "area_sq_km": 38464
    },
    {
        "id": "c0000005-0000-0000-0000-000000000001",
        "name": "Nagpur Rural",
        "name_local": "Nagpur Rural",
        "code": "MH-NAG-RUR",
        "level": "block",
        "parent_id": "b0000002-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Nagpur",
        "latitude": 21.15,
        "longitude": 79.05,
        "elevation_m": 310,
        "area_sq_km": 450
    },
    {
        "id": "c0000006-0000-0000-0000-000000000001",
        "name": "Kamptee",
        "name_local": "Kamptee",
        "code": "MH-NAG-KAM",
        "level": "block",
        "parent_id": "b0000002-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Nagpur",
        "latitude": 21.23,
        "longitude": 79.2,
        "elevation_m": 290,
        "area_sq_km": 450
    },
    {
        "id": "b0000003-0000-0000-0000-000000000001",
        "name": "Nashik",
        "name_local": "नाशिक",
        "code": "MH-NAS",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 20.0,
        "longitude": 73.78,
        "elevation_m": 700,
        "area_sq_km": 38464
    },
    {
        "id": "c0000007-0000-0000-0000-000000000001",
        "name": "Igatpuri",
        "name_local": "Igatpuri",
        "code": "MH-NAS-IGT",
        "level": "block",
        "parent_id": "b0000003-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Nashik",
        "latitude": 19.69,
        "longitude": 73.56,
        "elevation_m": 900,
        "area_sq_km": 450
    },
    {
        "id": "c0000008-0000-0000-0000-000000000001",
        "name": "Malegaon",
        "name_local": "Malegaon",
        "code": "MH-NAS-MAL",
        "level": "block",
        "parent_id": "b0000003-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Nashik",
        "latitude": 20.55,
        "longitude": 74.53,
        "elevation_m": 480,
        "area_sq_km": 450
    },
    {
        "id": "b0000004-0000-0000-0000-000000000001",
        "name": "Aurangabad",
        "name_local": "औरंगाबाद",
        "code": "MH-AUR",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 19.8762,
        "longitude": 75.3433,
        "elevation_m": 570,
        "area_sq_km": 38464
    },
    {
        "id": "c0000009-0000-0000-0000-000000000001",
        "name": "Paithan",
        "name_local": "Paithan",
        "code": "MH-AUR-PAI",
        "level": "block",
        "parent_id": "b0000004-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Aurangabad",
        "latitude": 19.48,
        "longitude": 75.38,
        "elevation_m": 460,
        "area_sq_km": 450
    },
    {
        "id": "c0000010-0000-0000-0000-000000000001",
        "name": "Gangapur",
        "name_local": "Gangapur",
        "code": "MH-AUR-GAN",
        "level": "block",
        "parent_id": "b0000004-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Aurangabad",
        "latitude": 19.7,
        "longitude": 75.01,
        "elevation_m": 510,
        "area_sq_km": 450
    },
    {
        "id": "b0000005-0000-0000-0000-000000000001",
        "name": "Kolhapur",
        "name_local": "कोल्हापूर",
        "code": "MH-KOL",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 16.705,
        "longitude": 74.2433,
        "elevation_m": 569,
        "area_sq_km": 38464
    },
    {
        "id": "c0000011-0000-0000-0000-000000000001",
        "name": "Karvir",
        "name_local": "Karvir",
        "code": "MH-KOL-KAR",
        "level": "block",
        "parent_id": "b0000005-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Kolhapur",
        "latitude": 16.68,
        "longitude": 74.22,
        "elevation_m": 550,
        "area_sq_km": 450
    },
    {
        "id": "c0000012-0000-0000-0000-000000000001",
        "name": "Hatkanangale",
        "name_local": "Hatkanangale",
        "code": "MH-KOL-HAT",
        "level": "block",
        "parent_id": "b0000005-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Kolhapur",
        "latitude": 16.75,
        "longitude": 74.45,
        "elevation_m": 570,
        "area_sq_km": 450
    },
    {
        "id": "b0000006-0000-0000-0000-000000000001",
        "name": "Solapur",
        "name_local": "सोलापूर",
        "code": "MH-SOL",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 17.6599,
        "longitude": 75.9064,
        "elevation_m": 458,
        "area_sq_km": 38464
    },
    {
        "id": "c0000013-0000-0000-0000-000000000001",
        "name": "Barshi",
        "name_local": "Barshi",
        "code": "MH-SOL-BAR",
        "level": "block",
        "parent_id": "b0000006-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Solapur",
        "latitude": 18.23,
        "longitude": 75.69,
        "elevation_m": 515,
        "area_sq_km": 450
    },
    {
        "id": "c0000014-0000-0000-0000-000000000001",
        "name": "Pandharpur",
        "name_local": "Pandharpur",
        "code": "MH-SOL-PAN",
        "level": "block",
        "parent_id": "b0000006-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Solapur",
        "latitude": 17.67,
        "longitude": 75.32,
        "elevation_m": 450,
        "area_sq_km": 450
    },
    {
        "id": "b0000007-0000-0000-0000-000000000001",
        "name": "Satara",
        "name_local": "सातारा",
        "code": "MH-SAT",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 17.6805,
        "longitude": 74.0183,
        "elevation_m": 750,
        "area_sq_km": 38464
    },
    {
        "id": "c0000015-0000-0000-0000-000000000001",
        "name": "Karad",
        "name_local": "Karad",
        "code": "MH-SAT-KRD",
        "level": "block",
        "parent_id": "b0000007-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Satara",
        "latitude": 17.28,
        "longitude": 74.2,
        "elevation_m": 580,
        "area_sq_km": 450
    },
    {
        "id": "c0000016-0000-0000-0000-000000000001",
        "name": "Wai",
        "name_local": "Wai",
        "code": "MH-SAT-WAI",
        "level": "block",
        "parent_id": "b0000007-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Satara",
        "latitude": 17.95,
        "longitude": 73.89,
        "elevation_m": 718,
        "area_sq_km": 450
    },
    {
        "id": "b0000008-0000-0000-0000-000000000001",
        "name": "Ahmednagar",
        "name_local": "अहमदनगर",
        "code": "MH-AHM",
        "level": "district",
        "parent_id": "a0000001-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": None,
        "latitude": 19.0948,
        "longitude": 74.748,
        "elevation_m": 649,
        "area_sq_km": 38464
    },
    {
        "id": "c0000017-0000-0000-0000-000000000001",
        "name": "Shrirampur",
        "name_local": "Shrirampur",
        "code": "MH-AHM-SHR",
        "level": "block",
        "parent_id": "b0000008-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Ahmednagar",
        "latitude": 19.62,
        "longitude": 74.65,
        "elevation_m": 520,
        "area_sq_km": 450
    },
    {
        "id": "c0000018-0000-0000-0000-000000000001",
        "name": "Sangamner",
        "name_local": "Sangamner",
        "code": "MH-AHM-SNG",
        "level": "block",
        "parent_id": "b0000008-0000-0000-0000-000000000001",
        "state_code": "MH",
        "state_name": "Maharashtra",
        "district_name": "Ahmednagar",
        "latitude": 19.57,
        "longitude": 74.21,
        "elevation_m": 549,
        "area_sq_km": 450
    },
    {
        "id": "b0000009-0000-0000-0000-000000000001",
        "name": "Belagavi",
        "name_local": "ಬೆಳಗಾವಿ",
        "code": "KA-BEL",
        "level": "district",
        "parent_id": "a0000002-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": None,
        "latitude": 15.8497,
        "longitude": 74.4977,
        "elevation_m": 762,
        "area_sq_km": 47948
    },
    {
        "id": "c0000019-0000-0000-0000-000000000001",
        "name": "Chikkodi",
        "name_local": "Chikkodi",
        "code": "KA-BEL-CHK",
        "level": "block",
        "parent_id": "b0000009-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Belagavi",
        "latitude": 16.43,
        "longitude": 74.59,
        "elevation_m": 610,
        "area_sq_km": 450
    },
    {
        "id": "c0000020-0000-0000-0000-000000000001",
        "name": "Gokak",
        "name_local": "Gokak",
        "code": "KA-BEL-GOK",
        "level": "block",
        "parent_id": "b0000009-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Belagavi",
        "latitude": 16.16,
        "longitude": 74.82,
        "elevation_m": 580,
        "area_sq_km": 450
    },
    {
        "id": "b0000010-0000-0000-0000-000000000001",
        "name": "Dharwad",
        "name_local": "ಧಾರವಾಡ",
        "code": "KA-DHA",
        "level": "district",
        "parent_id": "a0000002-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": None,
        "latitude": 15.4589,
        "longitude": 75.0078,
        "elevation_m": 750,
        "area_sq_km": 47948
    },
    {
        "id": "c0000021-0000-0000-0000-000000000001",
        "name": "Hubballi",
        "name_local": "Hubballi",
        "code": "KA-DHA-HUB",
        "level": "block",
        "parent_id": "b0000010-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Dharwad",
        "latitude": 15.3647,
        "longitude": 75.124,
        "elevation_m": 670,
        "area_sq_km": 450
    },
    {
        "id": "c0000022-0000-0000-0000-000000000001",
        "name": "Dharwad Rural",
        "name_local": "Dharwad Rural",
        "code": "KA-DHA-RUR",
        "level": "block",
        "parent_id": "b0000010-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Dharwad",
        "latitude": 15.48,
        "longitude": 74.98,
        "elevation_m": 720,
        "area_sq_km": 450
    },
    {
        "id": "b0000011-0000-0000-0000-000000000001",
        "name": "Raichur",
        "name_local": "ರಾಯಚೂರು",
        "code": "KA-RAI",
        "level": "district",
        "parent_id": "a0000002-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": None,
        "latitude": 16.2076,
        "longitude": 77.3463,
        "elevation_m": 407,
        "area_sq_km": 47948
    },
    {
        "id": "c0000023-0000-0000-0000-000000000001",
        "name": "Sindhanur",
        "name_local": "Sindhanur",
        "code": "KA-RAI-SIN",
        "level": "block",
        "parent_id": "b0000011-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Raichur",
        "latitude": 15.77,
        "longitude": 76.76,
        "elevation_m": 390,
        "area_sq_km": 450
    },
    {
        "id": "c0000024-0000-0000-0000-000000000001",
        "name": "Manvi",
        "name_local": "Manvi",
        "code": "KA-RAI-MAN",
        "level": "block",
        "parent_id": "b0000011-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Raichur",
        "latitude": 15.99,
        "longitude": 77.05,
        "elevation_m": 410,
        "area_sq_km": 450
    },
    {
        "id": "b0000012-0000-0000-0000-000000000001",
        "name": "Bengaluru Rural",
        "name_local": "ಬೆಂಗಳೂರು ಗ್ರಾಮಾಂತರ",
        "code": "KA-BLR",
        "level": "district",
        "parent_id": "a0000002-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": None,
        "latitude": 13.2285,
        "longitude": 77.5824,
        "elevation_m": 920,
        "area_sq_km": 47948
    },
    {
        "id": "c0000025-0000-0000-0000-000000000001",
        "name": "Devanahalli",
        "name_local": "Devanahalli",
        "code": "KA-BLR-DEV",
        "level": "block",
        "parent_id": "b0000012-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Bengaluru Rural",
        "latitude": 13.2483,
        "longitude": 77.7126,
        "elevation_m": 880,
        "area_sq_km": 450
    },
    {
        "id": "c0000026-0000-0000-0000-000000000001",
        "name": "Nelamangala",
        "name_local": "Nelamangala",
        "code": "KA-BLR-NEL",
        "level": "block",
        "parent_id": "b0000012-0000-0000-0000-000000000001",
        "state_code": "KA",
        "state_name": "Karnataka",
        "district_name": "Bengaluru Rural",
        "latitude": 13.098,
        "longitude": 77.391,
        "elevation_m": 882,
        "area_sq_km": 450
    },
    {
        "id": "b0000013-0000-0000-0000-000000000001",
        "name": "Ahmedabad",
        "name_local": "અમદાવાદ",
        "code": "GJ-AHM",
        "level": "district",
        "parent_id": "a0000003-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": None,
        "latitude": 23.0225,
        "longitude": 72.5714,
        "elevation_m": 53,
        "area_sq_km": 49006
    },
    {
        "id": "c0000027-0000-0000-0000-000000000001",
        "name": "Sanand",
        "name_local": "Sanand",
        "code": "GJ-AHM-SAN",
        "level": "block",
        "parent_id": "b0000013-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Ahmedabad",
        "latitude": 22.98,
        "longitude": 72.38,
        "elevation_m": 50,
        "area_sq_km": 450
    },
    {
        "id": "c0000028-0000-0000-0000-000000000001",
        "name": "Dholka",
        "name_local": "Dholka",
        "code": "GJ-AHM-DHO",
        "level": "block",
        "parent_id": "b0000013-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Ahmedabad",
        "latitude": 22.72,
        "longitude": 72.44,
        "elevation_m": 35,
        "area_sq_km": 450
    },
    {
        "id": "b0000014-0000-0000-0000-000000000001",
        "name": "Rajkot",
        "name_local": "રાજકોટ",
        "code": "GJ-RAJ",
        "level": "district",
        "parent_id": "a0000003-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": None,
        "latitude": 22.3039,
        "longitude": 70.8022,
        "elevation_m": 138,
        "area_sq_km": 49006
    },
    {
        "id": "c0000029-0000-0000-0000-000000000001",
        "name": "Gondal",
        "name_local": "Gondal",
        "code": "GJ-RAJ-GON",
        "level": "block",
        "parent_id": "b0000014-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Rajkot",
        "latitude": 21.96,
        "longitude": 70.8,
        "elevation_m": 125,
        "area_sq_km": 450
    },
    {
        "id": "c0000030-0000-0000-0000-000000000001",
        "name": "Jasdan",
        "name_local": "Jasdan",
        "code": "GJ-RAJ-JAS",
        "level": "block",
        "parent_id": "b0000014-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Rajkot",
        "latitude": 22.03,
        "longitude": 71.2,
        "elevation_m": 190,
        "area_sq_km": 450
    },
    {
        "id": "b0000015-0000-0000-0000-000000000001",
        "name": "Anand",
        "name_local": "આણંદ",
        "code": "GJ-AND",
        "level": "district",
        "parent_id": "a0000003-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": None,
        "latitude": 22.5645,
        "longitude": 72.9289,
        "elevation_m": 39,
        "area_sq_km": 49006
    },
    {
        "id": "c0000031-0000-0000-0000-000000000001",
        "name": "Petlad",
        "name_local": "Petlad",
        "code": "GJ-AND-PET",
        "level": "block",
        "parent_id": "b0000015-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Anand",
        "latitude": 22.47,
        "longitude": 72.8,
        "elevation_m": 35,
        "area_sq_km": 450
    },
    {
        "id": "c0000032-0000-0000-0000-000000000001",
        "name": "Borsad",
        "name_local": "Borsad",
        "code": "GJ-AND-BOR",
        "level": "block",
        "parent_id": "b0000015-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Anand",
        "latitude": 22.41,
        "longitude": 72.9,
        "elevation_m": 32,
        "area_sq_km": 450
    },
    {
        "id": "b0000016-0000-0000-0000-000000000001",
        "name": "Surat",
        "name_local": "સુરત",
        "code": "GJ-SUR",
        "level": "district",
        "parent_id": "a0000003-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": None,
        "latitude": 21.1702,
        "longitude": 72.8311,
        "elevation_m": 13,
        "area_sq_km": 49006
    },
    {
        "id": "c0000033-0000-0000-0000-000000000001",
        "name": "Bardoli",
        "name_local": "Bardoli",
        "code": "GJ-SUR-BAR",
        "level": "block",
        "parent_id": "b0000016-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Surat",
        "latitude": 21.12,
        "longitude": 73.11,
        "elevation_m": 22,
        "area_sq_km": 450
    },
    {
        "id": "c0000034-0000-0000-0000-000000000001",
        "name": "Olpad",
        "name_local": "Olpad",
        "code": "GJ-SUR-OLP",
        "level": "block",
        "parent_id": "b0000016-0000-0000-0000-000000000001",
        "state_code": "GJ",
        "state_name": "Gujarat",
        "district_name": "Surat",
        "latitude": 21.33,
        "longitude": 72.75,
        "elevation_m": 12,
        "area_sq_km": 450
    },
    {
        "id": "b0000017-0000-0000-0000-000000000001",
        "name": "Indore",
        "name_local": "इंदौर",
        "code": "MP-IND",
        "level": "district",
        "parent_id": "a0000004-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": None,
        "latitude": 22.7196,
        "longitude": 75.8577,
        "elevation_m": 553,
        "area_sq_km": 77063
    },
    {
        "id": "c0000035-0000-0000-0000-000000000001",
        "name": "Mhow",
        "name_local": "Mhow",
        "code": "MP-IND-MHO",
        "level": "block",
        "parent_id": "b0000017-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Indore",
        "latitude": 22.55,
        "longitude": 75.76,
        "elevation_m": 580,
        "area_sq_km": 450
    },
    {
        "id": "c0000036-0000-0000-0000-000000000001",
        "name": "Depalpur",
        "name_local": "Depalpur",
        "code": "MP-IND-DEP",
        "level": "block",
        "parent_id": "b0000017-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Indore",
        "latitude": 22.85,
        "longitude": 75.55,
        "elevation_m": 540,
        "area_sq_km": 450
    },
    {
        "id": "b0000018-0000-0000-0000-000000000001",
        "name": "Ujjain",
        "name_local": "उज्जैन",
        "code": "MP-UJJ",
        "level": "district",
        "parent_id": "a0000004-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": None,
        "latitude": 23.1765,
        "longitude": 75.7885,
        "elevation_m": 494,
        "area_sq_km": 77063
    },
    {
        "id": "c0000037-0000-0000-0000-000000000001",
        "name": "Nagda",
        "name_local": "Nagda",
        "code": "MP-UJJ-NAG",
        "level": "block",
        "parent_id": "b0000018-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Ujjain",
        "latitude": 23.45,
        "longitude": 75.41,
        "elevation_m": 480,
        "area_sq_km": 450
    },
    {
        "id": "c0000038-0000-0000-0000-000000000001",
        "name": "Badnagar",
        "name_local": "Badnagar",
        "code": "MP-UJJ-BAD",
        "level": "block",
        "parent_id": "b0000018-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Ujjain",
        "latitude": 23.01,
        "longitude": 75.38,
        "elevation_m": 500,
        "area_sq_km": 450
    },
    {
        "id": "b0000019-0000-0000-0000-000000000001",
        "name": "Bhopal",
        "name_local": "भोपाल",
        "code": "MP-BHO",
        "level": "district",
        "parent_id": "a0000004-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": None,
        "latitude": 23.2599,
        "longitude": 77.4126,
        "elevation_m": 527,
        "area_sq_km": 77063
    },
    {
        "id": "c0000039-0000-0000-0000-000000000001",
        "name": "Berasia",
        "name_local": "Berasia",
        "code": "MP-BHO-BER",
        "level": "block",
        "parent_id": "b0000019-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Bhopal",
        "latitude": 23.63,
        "longitude": 77.43,
        "elevation_m": 480,
        "area_sq_km": 450
    },
    {
        "id": "c0000040-0000-0000-0000-000000000001",
        "name": "Phanda",
        "name_local": "Phanda",
        "code": "MP-BHO-PHA",
        "level": "block",
        "parent_id": "b0000019-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Bhopal",
        "latitude": 23.18,
        "longitude": 77.28,
        "elevation_m": 510,
        "area_sq_km": 450
    },
    {
        "id": "b0000020-0000-0000-0000-000000000001",
        "name": "Hoshangabad",
        "name_local": "नर्मदापुरम",
        "code": "MP-HOS",
        "level": "district",
        "parent_id": "a0000004-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": None,
        "latitude": 22.7519,
        "longitude": 77.7289,
        "elevation_m": 302,
        "area_sq_km": 77063
    },
    {
        "id": "c0000041-0000-0000-0000-000000000001",
        "name": "Itarsi",
        "name_local": "Itarsi",
        "code": "MP-HOS-ITA",
        "level": "block",
        "parent_id": "b0000020-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Hoshangabad",
        "latitude": 22.61,
        "longitude": 77.76,
        "elevation_m": 310,
        "area_sq_km": 450
    },
    {
        "id": "c0000042-0000-0000-0000-000000000001",
        "name": "Pipariya",
        "name_local": "Pipariya",
        "code": "MP-HOS-PIP",
        "level": "block",
        "parent_id": "b0000020-0000-0000-0000-000000000001",
        "state_code": "MP",
        "state_name": "Madhya Pradesh",
        "district_name": "Hoshangabad",
        "latitude": 22.76,
        "longitude": 78.35,
        "elevation_m": 330,
        "area_sq_km": 450
    },
    {
        "id": "b0000021-0000-0000-0000-000000000001",
        "name": "Ludhiana",
        "name_local": "ਲੁਧਿਆਣਾ",
        "code": "PB-LUD",
        "level": "district",
        "parent_id": "a0000005-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": None,
        "latitude": 30.901,
        "longitude": 75.8573,
        "elevation_m": 244,
        "area_sq_km": 12590
    },
    {
        "id": "c0000043-0000-0000-0000-000000000001",
        "name": "Jagraon",
        "name_local": "Jagraon",
        "code": "PB-LUD-JAG",
        "level": "block",
        "parent_id": "b0000021-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Ludhiana",
        "latitude": 30.79,
        "longitude": 75.48,
        "elevation_m": 235,
        "area_sq_km": 450
    },
    {
        "id": "c0000044-0000-0000-0000-000000000001",
        "name": "Khanna",
        "name_local": "Khanna",
        "code": "PB-LUD-KHA",
        "level": "block",
        "parent_id": "b0000021-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Ludhiana",
        "latitude": 30.7,
        "longitude": 76.22,
        "elevation_m": 255,
        "area_sq_km": 450
    },
    {
        "id": "b0000022-0000-0000-0000-000000000001",
        "name": "Amritsar",
        "name_local": "ਅੰਮ੍ਰਿਤਸਰ",
        "code": "PB-AMR",
        "level": "district",
        "parent_id": "a0000005-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": None,
        "latitude": 31.634,
        "longitude": 74.8723,
        "elevation_m": 234,
        "area_sq_km": 12590
    },
    {
        "id": "c0000045-0000-0000-0000-000000000001",
        "name": "Ajnala",
        "name_local": "Ajnala",
        "code": "PB-AMR-AJN",
        "level": "block",
        "parent_id": "b0000022-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Amritsar",
        "latitude": 31.84,
        "longitude": 74.76,
        "elevation_m": 225,
        "area_sq_km": 450
    },
    {
        "id": "c0000046-0000-0000-0000-000000000001",
        "name": "Majitha",
        "name_local": "Majitha",
        "code": "PB-AMR-MAJ",
        "level": "block",
        "parent_id": "b0000022-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Amritsar",
        "latitude": 31.76,
        "longitude": 74.96,
        "elevation_m": 235,
        "area_sq_km": 450
    },
    {
        "id": "b0000023-0000-0000-0000-000000000001",
        "name": "Patiala",
        "name_local": "ਪਟਿਆਲਾ",
        "code": "PB-PAT",
        "level": "district",
        "parent_id": "a0000005-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": None,
        "latitude": 30.3398,
        "longitude": 76.3869,
        "elevation_m": 250,
        "area_sq_km": 12590
    },
    {
        "id": "c0000047-0000-0000-0000-000000000001",
        "name": "Nabha",
        "name_local": "Nabha",
        "code": "PB-PAT-NAB",
        "level": "block",
        "parent_id": "b0000023-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Patiala",
        "latitude": 30.37,
        "longitude": 76.15,
        "elevation_m": 248,
        "area_sq_km": 450
    },
    {
        "id": "c0000048-0000-0000-0000-000000000001",
        "name": "Rajpura",
        "name_local": "Rajpura",
        "code": "PB-PAT-RAJ",
        "level": "block",
        "parent_id": "b0000023-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Patiala",
        "latitude": 30.48,
        "longitude": 76.6,
        "elevation_m": 260,
        "area_sq_km": 450
    },
    {
        "id": "b0000024-0000-0000-0000-000000000001",
        "name": "Bathinda",
        "name_local": "ਬਠਿੰਡਾ",
        "code": "PB-BAT",
        "level": "district",
        "parent_id": "a0000005-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": None,
        "latitude": 30.211,
        "longitude": 74.9455,
        "elevation_m": 201,
        "area_sq_km": 12590
    },
    {
        "id": "c0000049-0000-0000-0000-000000000001",
        "name": "Talwandi Sabo",
        "name_local": "Talwandi Sabo",
        "code": "PB-BAT-TAL",
        "level": "block",
        "parent_id": "b0000024-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Bathinda",
        "latitude": 29.98,
        "longitude": 75.09,
        "elevation_m": 208,
        "area_sq_km": 450
    },
    {
        "id": "c0000050-0000-0000-0000-000000000001",
        "name": "Rampura Phul",
        "name_local": "Rampura Phul",
        "code": "PB-BAT-RAM",
        "level": "block",
        "parent_id": "b0000024-0000-0000-0000-000000000001",
        "state_code": "PB",
        "state_name": "Punjab",
        "district_name": "Bathinda",
        "latitude": 30.27,
        "longitude": 75.24,
        "elevation_m": 215,
        "area_sq_km": 450
    },
    {
        "id": "b0000025-0000-0000-0000-000000000001",
        "name": "Varanasi",
        "name_local": "वाराणसी",
        "code": "UP-VAR",
        "level": "district",
        "parent_id": "a0000006-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": None,
        "latitude": 25.3176,
        "longitude": 82.9739,
        "elevation_m": 81,
        "area_sq_km": 60232
    },
    {
        "id": "c0000051-0000-0000-0000-000000000001",
        "name": "Pindra",
        "name_local": "Pindra",
        "code": "UP-VAR-PIN",
        "level": "block",
        "parent_id": "b0000025-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Varanasi",
        "latitude": 25.52,
        "longitude": 82.85,
        "elevation_m": 85,
        "area_sq_km": 450
    },
    {
        "id": "c0000052-0000-0000-0000-000000000001",
        "name": "Cholapur",
        "name_local": "Cholapur",
        "code": "UP-VAR-CHO",
        "level": "block",
        "parent_id": "b0000025-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Varanasi",
        "latitude": 25.46,
        "longitude": 83.05,
        "elevation_m": 82,
        "area_sq_km": 450
    },
    {
        "id": "b0000026-0000-0000-0000-000000000001",
        "name": "Lucknow",
        "name_local": "लखनऊ",
        "code": "UP-LUK",
        "level": "district",
        "parent_id": "a0000006-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": None,
        "latitude": 26.8467,
        "longitude": 80.9462,
        "elevation_m": 123,
        "area_sq_km": 60232
    },
    {
        "id": "c0000053-0000-0000-0000-000000000001",
        "name": "Bakshi Ka Talab",
        "name_local": "Bakshi Ka Talab",
        "code": "UP-LUK-BKT",
        "level": "block",
        "parent_id": "b0000026-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Lucknow",
        "latitude": 27.02,
        "longitude": 80.93,
        "elevation_m": 125,
        "area_sq_km": 450
    },
    {
        "id": "c0000054-0000-0000-0000-000000000001",
        "name": "Mohanlalganj",
        "name_local": "Mohanlalganj",
        "code": "UP-LUK-MOH",
        "level": "block",
        "parent_id": "b0000026-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Lucknow",
        "latitude": 26.68,
        "longitude": 80.98,
        "elevation_m": 120,
        "area_sq_km": 450
    },
    {
        "id": "b0000027-0000-0000-0000-000000000001",
        "name": "Gorakhpur",
        "name_local": "गोरखपुर",
        "code": "UP-GOR",
        "level": "district",
        "parent_id": "a0000006-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": None,
        "latitude": 26.7606,
        "longitude": 83.3732,
        "elevation_m": 84,
        "area_sq_km": 60232
    },
    {
        "id": "c0000055-0000-0000-0000-000000000001",
        "name": "Sahjanwa",
        "name_local": "Sahjanwa",
        "code": "UP-GOR-SAH",
        "level": "block",
        "parent_id": "b0000027-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Gorakhpur",
        "latitude": 26.77,
        "longitude": 83.19,
        "elevation_m": 84,
        "area_sq_km": 450
    },
    {
        "id": "c0000056-0000-0000-0000-000000000001",
        "name": "Campierganj",
        "name_local": "Campierganj",
        "code": "UP-GOR-CAM",
        "level": "block",
        "parent_id": "b0000027-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Gorakhpur",
        "latitude": 27.02,
        "longitude": 83.27,
        "elevation_m": 88,
        "area_sq_km": 450
    },
    {
        "id": "b0000028-0000-0000-0000-000000000001",
        "name": "Prayagraj",
        "name_local": "प्रयागराज",
        "code": "UP-PRY",
        "level": "district",
        "parent_id": "a0000006-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": None,
        "latitude": 25.4358,
        "longitude": 81.8463,
        "elevation_m": 98,
        "area_sq_km": 60232
    },
    {
        "id": "c0000057-0000-0000-0000-000000000001",
        "name": "Phulpur",
        "name_local": "Phulpur",
        "code": "UP-PRY-PHU",
        "level": "block",
        "parent_id": "b0000028-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Prayagraj",
        "latitude": 25.55,
        "longitude": 82.08,
        "elevation_m": 96,
        "area_sq_km": 450
    },
    {
        "id": "c0000058-0000-0000-0000-000000000001",
        "name": "Koraon",
        "name_local": "Koraon",
        "code": "UP-PRY-KOR",
        "level": "block",
        "parent_id": "b0000028-0000-0000-0000-000000000001",
        "state_code": "UP",
        "state_name": "Uttar Pradesh",
        "district_name": "Prayagraj",
        "latitude": 24.98,
        "longitude": 82.07,
        "elevation_m": 125,
        "area_sq_km": 450
    },
    {
        "id": "b0000029-0000-0000-0000-000000000001",
        "name": "Visakhapatnam",
        "name_local": "విశాఖపట్నం",
        "code": "AP-VIS",
        "level": "district",
        "parent_id": "a0000007-0000-0000-0000-000000000001",
        "state_code": "AP",
        "state_name": "Andhra Pradesh",
        "district_name": None,
        "latitude": 17.6868,
        "longitude": 83.2185,
        "elevation_m": 45,
        "area_sq_km": 81484
    },
    {
        "id": "c0000059-0000-0000-0000-000000000001",
        "name": "Anakapalle",
        "name_local": "Anakapalle",
        "code": "AP-VIS-ANA",
        "level": "block",
        "parent_id": "b0000029-0000-0000-0000-000000000001",
        "state_code": "AP",
        "state_name": "Andhra Pradesh",
        "district_name": "Visakhapatnam",
        "latitude": 17.6913,
        "longitude": 83.0039,
        "elevation_m": 26,
        "area_sq_km": 450
    },
    {
        "id": "c0000060-0000-0000-0000-000000000001",
        "name": "Bheemunipatnam",
        "name_local": "Bheemunipatnam",
        "code": "AP-VIS-BHE",
        "level": "block",
        "parent_id": "b0000029-0000-0000-0000-000000000001",
        "state_code": "AP",
        "state_name": "Andhra Pradesh",
        "district_name": "Visakhapatnam",
        "latitude": 17.8906,
        "longitude": 83.4542,
        "elevation_m": 12,
        "area_sq_km": 450
    },
    {
        "id": "b0000030-0000-0000-0000-000000000001",
        "name": "Guntur",
        "name_local": "గుంటూరు",
        "code": "AP-GUN",
        "level": "district",
        "parent_id": "a0000007-0000-0000-0000-000000000001",
        "state_code": "AP",
        "state_name": "Andhra Pradesh",
        "district_name": None,
        "latitude": 16.3067,
        "longitude": 80.4365,
        "elevation_m": 33,
        "area_sq_km": 81484
    },
    {
        "id": "c0000061-0000-0000-0000-000000000001",
        "name": "Tenali",
        "name_local": "Tenali",
        "code": "AP-GUN-TEN",
        "level": "block",
        "parent_id": "b0000030-0000-0000-0000-000000000001",
        "state_code": "AP",
        "state_name": "Andhra Pradesh",
        "district_name": "Guntur",
        "latitude": 16.243,
        "longitude": 80.64,
        "elevation_m": 15,
        "area_sq_km": 450
    },
    {
        "id": "c0000062-0000-0000-0000-000000000001",
        "name": "Mangalagiri",
        "name_local": "Mangalagiri",
        "code": "AP-GUN-MAN",
        "level": "block",
        "parent_id": "b0000030-0000-0000-0000-000000000001",
        "state_code": "AP",
        "state_name": "Andhra Pradesh",
        "district_name": "Guntur",
        "latitude": 16.43,
        "longitude": 80.57,
        "elevation_m": 24,
        "area_sq_km": 450
    },
    {
        "id": "b0000031-0000-0000-0000-000000000001",
        "name": "Papum Pare",
        "name_local": "পাপুম পাৰে",
        "code": "AR-PAP",
        "level": "district",
        "parent_id": "a0000008-0000-0000-0000-000000000001",
        "state_code": "AR",
        "state_name": "Arunachal Pradesh",
        "district_name": None,
        "latitude": 27.1004,
        "longitude": 93.6166,
        "elevation_m": 320,
        "area_sq_km": 83743
    },
    {
        "id": "c0000063-0000-0000-0000-000000000001",
        "name": "Itanagar",
        "name_local": "Itanagar",
        "code": "AR-PAP-ITA",
        "level": "block",
        "parent_id": "b0000031-0000-0000-0000-000000000001",
        "state_code": "AR",
        "state_name": "Arunachal Pradesh",
        "district_name": "Papum Pare",
        "latitude": 27.0844,
        "longitude": 93.6053,
        "elevation_m": 320,
        "area_sq_km": 450
    },
    {
        "id": "c0000064-0000-0000-0000-000000000001",
        "name": "Naharlagun",
        "name_local": "Naharlagun",
        "code": "AR-PAP-NAH",
        "level": "block",
        "parent_id": "b0000031-0000-0000-0000-000000000001",
        "state_code": "AR",
        "state_name": "Arunachal Pradesh",
        "district_name": "Papum Pare",
        "latitude": 27.1056,
        "longitude": 93.6934,
        "elevation_m": 290,
        "area_sq_km": 450
    },
    {
        "id": "b0000032-0000-0000-0000-000000000001",
        "name": "Kamrup",
        "name_local": "কামৰূপ",
        "code": "AS-KAM",
        "level": "district",
        "parent_id": "a0000009-0000-0000-0000-000000000001",
        "state_code": "AS",
        "state_name": "Assam",
        "district_name": None,
        "latitude": 26.3161,
        "longitude": 91.5984,
        "elevation_m": 55,
        "area_sq_km": 39219
    },
    {
        "id": "c0000065-0000-0000-0000-000000000001",
        "name": "Rangia",
        "name_local": "Rangia",
        "code": "AS-KAM-RAN",
        "level": "block",
        "parent_id": "b0000032-0000-0000-0000-000000000001",
        "state_code": "AS",
        "state_name": "Assam",
        "district_name": "Kamrup",
        "latitude": 26.4673,
        "longitude": 91.6288,
        "elevation_m": 52,
        "area_sq_km": 450
    },
    {
        "id": "c0000066-0000-0000-0000-000000000001",
        "name": "Hajo",
        "name_local": "Hajo",
        "code": "AS-KAM-HAJ",
        "level": "block",
        "parent_id": "b0000032-0000-0000-0000-000000000001",
        "state_code": "AS",
        "state_name": "Assam",
        "district_name": "Kamrup",
        "latitude": 26.2482,
        "longitude": 91.5284,
        "elevation_m": 50,
        "area_sq_km": 450
    },
    {
        "id": "b0000033-0000-0000-0000-000000000001",
        "name": "Dibrugarh",
        "name_local": "ডিব্ৰুগড়",
        "code": "AS-DIB",
        "level": "district",
        "parent_id": "a0000009-0000-0000-0000-000000000001",
        "state_code": "AS",
        "state_name": "Assam",
        "district_name": None,
        "latitude": 27.4728,
        "longitude": 94.912,
        "elevation_m": 108,
        "area_sq_km": 39219
    },
    {
        "id": "c0000067-0000-0000-0000-000000000001",
        "name": "Moran",
        "name_local": "Moran",
        "code": "AS-DIB-MOR",
        "level": "block",
        "parent_id": "b0000033-0000-0000-0000-000000000001",
        "state_code": "AS",
        "state_name": "Assam",
        "district_name": "Dibrugarh",
        "latitude": 27.1856,
        "longitude": 94.9284,
        "elevation_m": 102,
        "area_sq_km": 450
    },
    {
        "id": "c0000068-0000-0000-0000-000000000001",
        "name": "Naharkatia",
        "name_local": "Naharkatia",
        "code": "AS-DIB-NAH",
        "level": "block",
        "parent_id": "b0000033-0000-0000-0000-000000000001",
        "state_code": "AS",
        "state_name": "Assam",
        "district_name": "Dibrugarh",
        "latitude": 27.2833,
        "longitude": 95.3333,
        "elevation_m": 120,
        "area_sq_km": 450
    },
    {
        "id": "b0000034-0000-0000-0000-000000000001",
        "name": "Patna",
        "name_local": "पटना",
        "code": "BR-PAT",
        "level": "district",
        "parent_id": "a0000010-0000-0000-0000-000000000001",
        "state_code": "BR",
        "state_name": "Bihar",
        "district_name": None,
        "latitude": 25.5941,
        "longitude": 85.1376,
        "elevation_m": 53,
        "area_sq_km": 47082
    },
    {
        "id": "c0000069-0000-0000-0000-000000000001",
        "name": "Danapur",
        "name_local": "Danapur",
        "code": "BR-PAT-DAN",
        "level": "block",
        "parent_id": "b0000034-0000-0000-0000-000000000001",
        "state_code": "BR",
        "state_name": "Bihar",
        "district_name": "Patna",
        "latitude": 25.63,
        "longitude": 85.04,
        "elevation_m": 52,
        "area_sq_km": 450
    },
    {
        "id": "c0000070-0000-0000-0000-000000000001",
        "name": "Phulwari Sharif",
        "name_local": "Phulwari Sharif",
        "code": "BR-PAT-PHU",
        "level": "block",
        "parent_id": "b0000034-0000-0000-0000-000000000001",
        "state_code": "BR",
        "state_name": "Bihar",
        "district_name": "Patna",
        "latitude": 25.57,
        "longitude": 85.08,
        "elevation_m": 53,
        "area_sq_km": 450
    },
    {
        "id": "b0000035-0000-0000-0000-000000000001",
        "name": "Muzaffarpur",
        "name_local": "मुज़फ़्फ़रपुर",
        "code": "BR-MUZ",
        "level": "district",
        "parent_id": "a0000010-0000-0000-0000-000000000001",
        "state_code": "BR",
        "state_name": "Bihar",
        "district_name": None,
        "latitude": 26.1209,
        "longitude": 85.3647,
        "elevation_m": 60,
        "area_sq_km": 47082
    },
    {
        "id": "c0000071-0000-0000-0000-000000000001",
        "name": "Kanti",
        "name_local": "Kanti",
        "code": "BR-MUZ-KAN",
        "level": "block",
        "parent_id": "b0000035-0000-0000-0000-000000000001",
        "state_code": "BR",
        "state_name": "Bihar",
        "district_name": "Muzaffarpur",
        "latitude": 26.2,
        "longitude": 85.3,
        "elevation_m": 58,
        "area_sq_km": 450
    },
    {
        "id": "c0000072-0000-0000-0000-000000000001",
        "name": "Marwan",
        "name_local": "Marwan",
        "code": "BR-MUZ-MAR",
        "level": "block",
        "parent_id": "b0000035-0000-0000-0000-000000000001",
        "state_code": "BR",
        "state_name": "Bihar",
        "district_name": "Muzaffarpur",
        "latitude": 26.13,
        "longitude": 85.27,
        "elevation_m": 59,
        "area_sq_km": 450
    },
    {
        "id": "b0000036-0000-0000-0000-000000000001",
        "name": "Raipur",
        "name_local": "रायपुर",
        "code": "CG-RAI",
        "level": "district",
        "parent_id": "a0000011-0000-0000-0000-000000000001",
        "state_code": "CG",
        "state_name": "Chhattisgarh",
        "district_name": None,
        "latitude": 21.2514,
        "longitude": 81.6296,
        "elevation_m": 298,
        "area_sq_km": 67596
    },
    {
        "id": "c0000073-0000-0000-0000-000000000001",
        "name": "Arang",
        "name_local": "Arang",
        "code": "CG-RAI-ARA",
        "level": "block",
        "parent_id": "b0000036-0000-0000-0000-000000000001",
        "state_code": "CG",
        "state_name": "Chhattisgarh",
        "district_name": "Raipur",
        "latitude": 21.19,
        "longitude": 81.96,
        "elevation_m": 285,
        "area_sq_km": 450
    },
    {
        "id": "c0000074-0000-0000-0000-000000000001",
        "name": "Abhanpur",
        "name_local": "Abhanpur",
        "code": "CG-RAI-ABH",
        "level": "block",
        "parent_id": "b0000036-0000-0000-0000-000000000001",
        "state_code": "CG",
        "state_name": "Chhattisgarh",
        "district_name": "Raipur",
        "latitude": 21.05,
        "longitude": 81.74,
        "elevation_m": 290,
        "area_sq_km": 450
    },
    {
        "id": "b0000037-0000-0000-0000-000000000001",
        "name": "Bilaspur",
        "name_local": "बिलासपुर",
        "code": "CG-BIL",
        "level": "district",
        "parent_id": "a0000011-0000-0000-0000-000000000001",
        "state_code": "CG",
        "state_name": "Chhattisgarh",
        "district_name": None,
        "latitude": 22.0797,
        "longitude": 82.1409,
        "elevation_m": 264,
        "area_sq_km": 67596
    },
    {
        "id": "c0000075-0000-0000-0000-000000000001",
        "name": "Kota",
        "name_local": "Kota",
        "code": "CG-BIL-KOT",
        "level": "block",
        "parent_id": "b0000037-0000-0000-0000-000000000001",
        "state_code": "CG",
        "state_name": "Chhattisgarh",
        "district_name": "Bilaspur",
        "latitude": 22.29,
        "longitude": 82.02,
        "elevation_m": 270,
        "area_sq_km": 450
    },
    {
        "id": "c0000076-0000-0000-0000-000000000001",
        "name": "Takhatpur",
        "name_local": "Takhatpur",
        "code": "CG-BIL-TAK",
        "level": "block",
        "parent_id": "b0000037-0000-0000-0000-000000000001",
        "state_code": "CG",
        "state_name": "Chhattisgarh",
        "district_name": "Bilaspur",
        "latitude": 22.14,
        "longitude": 81.86,
        "elevation_m": 260,
        "area_sq_km": 450
    },
    {
        "id": "b0000038-0000-0000-0000-000000000001",
        "name": "North Goa",
        "name_local": "उत्तर गोंय",
        "code": "GA-NGO",
        "level": "district",
        "parent_id": "a0000012-0000-0000-0000-000000000001",
        "state_code": "GA",
        "state_name": "Goa",
        "district_name": None,
        "latitude": 15.5527,
        "longitude": 73.8278,
        "elevation_m": 15,
        "area_sq_km": 1851
    },
    {
        "id": "c0000077-0000-0000-0000-000000000001",
        "name": "Bardez",
        "name_local": "Bardez",
        "code": "GA-NGO-BAR",
        "level": "block",
        "parent_id": "b0000038-0000-0000-0000-000000000001",
        "state_code": "GA",
        "state_name": "Goa",
        "district_name": "North Goa",
        "latitude": 15.59,
        "longitude": 73.81,
        "elevation_m": 18,
        "area_sq_km": 450
    },
    {
        "id": "c0000078-0000-0000-0000-000000000001",
        "name": "Tiswadi",
        "name_local": "Tiswadi",
        "code": "GA-NGO-TIS",
        "level": "block",
        "parent_id": "b0000038-0000-0000-0000-000000000001",
        "state_code": "GA",
        "state_name": "Goa",
        "district_name": "North Goa",
        "latitude": 15.49,
        "longitude": 73.86,
        "elevation_m": 10,
        "area_sq_km": 450
    },
    {
        "id": "b0000039-0000-0000-0000-000000000001",
        "name": "South Goa",
        "name_local": "दक्षिण गोंय",
        "code": "GA-SGO",
        "level": "district",
        "parent_id": "a0000012-0000-0000-0000-000000000001",
        "state_code": "GA",
        "state_name": "Goa",
        "district_name": None,
        "latitude": 15.2736,
        "longitude": 73.958,
        "elevation_m": 12,
        "area_sq_km": 1851
    },
    {
        "id": "c0000079-0000-0000-0000-000000000001",
        "name": "Salcete",
        "name_local": "Salcete",
        "code": "GA-SGO-SAL",
        "level": "block",
        "parent_id": "b0000039-0000-0000-0000-000000000001",
        "state_code": "GA",
        "state_name": "Goa",
        "district_name": "South Goa",
        "latitude": 15.28,
        "longitude": 73.96,
        "elevation_m": 14,
        "area_sq_km": 450
    },
    {
        "id": "c0000080-0000-0000-0000-000000000001",
        "name": "Ponda",
        "name_local": "Ponda",
        "code": "GA-SGO-PON",
        "level": "block",
        "parent_id": "b0000039-0000-0000-0000-000000000001",
        "state_code": "GA",
        "state_name": "Goa",
        "district_name": "South Goa",
        "latitude": 15.4,
        "longitude": 74.02,
        "elevation_m": 42,
        "area_sq_km": 450
    },
    {
        "id": "b0000040-0000-0000-0000-000000000001",
        "name": "Karnal",
        "name_local": "करनाल",
        "code": "HR-KAR",
        "level": "district",
        "parent_id": "a0000013-0000-0000-0000-000000000001",
        "state_code": "HR",
        "state_name": "Haryana",
        "district_name": None,
        "latitude": 29.6857,
        "longitude": 76.9905,
        "elevation_m": 228,
        "area_sq_km": 22106
    },
    {
        "id": "c0000081-0000-0000-0000-000000000001",
        "name": "Nilokheri",
        "name_local": "Nilokheri",
        "code": "HR-KAR-NIL",
        "level": "block",
        "parent_id": "b0000040-0000-0000-0000-000000000001",
        "state_code": "HR",
        "state_name": "Haryana",
        "district_name": "Karnal",
        "latitude": 29.83,
        "longitude": 76.92,
        "elevation_m": 235,
        "area_sq_km": 450
    },
    {
        "id": "c0000082-0000-0000-0000-000000000001",
        "name": "Gharaunda",
        "name_local": "Gharaunda",
        "code": "HR-KAR-GHA",
        "level": "block",
        "parent_id": "b0000040-0000-0000-0000-000000000001",
        "state_code": "HR",
        "state_name": "Haryana",
        "district_name": "Karnal",
        "latitude": 29.54,
        "longitude": 76.97,
        "elevation_m": 223,
        "area_sq_km": 450
    },
    {
        "id": "b0000041-0000-0000-0000-000000000001",
        "name": "Hisar",
        "name_local": "हिसार",
        "code": "HR-HIS",
        "level": "district",
        "parent_id": "a0000013-0000-0000-0000-000000000001",
        "state_code": "HR",
        "state_name": "Haryana",
        "district_name": None,
        "latitude": 29.1492,
        "longitude": 75.7217,
        "elevation_m": 215,
        "area_sq_km": 22106
    },
    {
        "id": "c0000083-0000-0000-0000-000000000001",
        "name": "Hansi",
        "name_local": "Hansi",
        "code": "HR-HIS-HAN",
        "level": "block",
        "parent_id": "b0000041-0000-0000-0000-000000000001",
        "state_code": "HR",
        "state_name": "Haryana",
        "district_name": "Hisar",
        "latitude": 29.1,
        "longitude": 75.96,
        "elevation_m": 212,
        "area_sq_km": 450
    },
    {
        "id": "c0000084-0000-0000-0000-000000000001",
        "name": "Barwala",
        "name_local": "Barwala",
        "code": "HR-HIS-BAR",
        "level": "block",
        "parent_id": "b0000041-0000-0000-0000-000000000001",
        "state_code": "HR",
        "state_name": "Haryana",
        "district_name": "Hisar",
        "latitude": 29.38,
        "longitude": 75.91,
        "elevation_m": 218,
        "area_sq_km": 450
    },
    {
        "id": "b0000042-0000-0000-0000-000000000001",
        "name": "Kangra",
        "name_local": "कांगड़ा",
        "code": "HP-KAN",
        "level": "district",
        "parent_id": "a0000014-0000-0000-0000-000000000001",
        "state_code": "HP",
        "state_name": "Himachal Pradesh",
        "district_name": None,
        "latitude": 32.0998,
        "longitude": 76.2691,
        "elevation_m": 733,
        "area_sq_km": 27836
    },
    {
        "id": "c0000085-0000-0000-0000-000000000001",
        "name": "Dharamshala",
        "name_local": "Dharamshala",
        "code": "HP-KAN-DHA",
        "level": "block",
        "parent_id": "b0000042-0000-0000-0000-000000000001",
        "state_code": "HP",
        "state_name": "Himachal Pradesh",
        "district_name": "Kangra",
        "latitude": 32.219,
        "longitude": 76.3234,
        "elevation_m": 1457,
        "area_sq_km": 450
    },
    {
        "id": "c0000086-0000-0000-0000-000000000001",
        "name": "Palampur",
        "name_local": "Palampur",
        "code": "HP-KAN-PAL",
        "level": "block",
        "parent_id": "b0000042-0000-0000-0000-000000000001",
        "state_code": "HP",
        "state_name": "Himachal Pradesh",
        "district_name": "Kangra",
        "latitude": 32.1109,
        "longitude": 76.5363,
        "elevation_m": 1220,
        "area_sq_km": 450
    },
    {
        "id": "b0000043-0000-0000-0000-000000000001",
        "name": "Shimla",
        "name_local": "शिमला",
        "code": "HP-SHI",
        "level": "district",
        "parent_id": "a0000014-0000-0000-0000-000000000001",
        "state_code": "HP",
        "state_name": "Himachal Pradesh",
        "district_name": None,
        "latitude": 31.1048,
        "longitude": 77.1734,
        "elevation_m": 2206,
        "area_sq_km": 27836
    },
    {
        "id": "c0000087-0000-0000-0000-000000000001",
        "name": "Theog",
        "name_local": "Theog",
        "code": "HP-SHI-THE",
        "level": "block",
        "parent_id": "b0000043-0000-0000-0000-000000000001",
        "state_code": "HP",
        "state_name": "Himachal Pradesh",
        "district_name": "Shimla",
        "latitude": 31.12,
        "longitude": 77.35,
        "elevation_m": 2280,
        "area_sq_km": 450
    },
    {
        "id": "c0000088-0000-0000-0000-000000000001",
        "name": "Rampur",
        "name_local": "Rampur",
        "code": "HP-SHI-RAM",
        "level": "block",
        "parent_id": "b0000043-0000-0000-0000-000000000001",
        "state_code": "HP",
        "state_name": "Himachal Pradesh",
        "district_name": "Shimla",
        "latitude": 31.45,
        "longitude": 77.63,
        "elevation_m": 1350,
        "area_sq_km": 450
    },
    {
        "id": "b0000044-0000-0000-0000-000000000001",
        "name": "Ranchi",
        "name_local": "राँची",
        "code": "JH-RAN",
        "level": "district",
        "parent_id": "a0000015-0000-0000-0000-000000000001",
        "state_code": "JH",
        "state_name": "Jharkhand",
        "district_name": None,
        "latitude": 23.3441,
        "longitude": 85.3096,
        "elevation_m": 651,
        "area_sq_km": 39858
    },
    {
        "id": "c0000089-0000-0000-0000-000000000001",
        "name": "Kanke",
        "name_local": "Kanke",
        "code": "JH-RAN-KAN",
        "level": "block",
        "parent_id": "b0000044-0000-0000-0000-000000000001",
        "state_code": "JH",
        "state_name": "Jharkhand",
        "district_name": "Ranchi",
        "latitude": 23.43,
        "longitude": 85.32,
        "elevation_m": 645,
        "area_sq_km": 450
    },
    {
        "id": "c0000090-0000-0000-0000-000000000001",
        "name": "Ormanjhi",
        "name_local": "Ormanjhi",
        "code": "JH-RAN-ORM",
        "level": "block",
        "parent_id": "b0000044-0000-0000-0000-000000000001",
        "state_code": "JH",
        "state_name": "Jharkhand",
        "district_name": "Ranchi",
        "latitude": 23.48,
        "longitude": 85.48,
        "elevation_m": 630,
        "area_sq_km": 450
    },
    {
        "id": "b0000045-0000-0000-0000-000000000001",
        "name": "Dhanbad",
        "name_local": "धनबाद",
        "code": "JH-DHA",
        "level": "district",
        "parent_id": "a0000015-0000-0000-0000-000000000001",
        "state_code": "JH",
        "state_name": "Jharkhand",
        "district_name": None,
        "latitude": 23.7957,
        "longitude": 86.4304,
        "elevation_m": 227,
        "area_sq_km": 39858
    },
    {
        "id": "c0000091-0000-0000-0000-000000000001",
        "name": "Govindpur",
        "name_local": "Govindpur",
        "code": "JH-DHA-GOV",
        "level": "block",
        "parent_id": "b0000045-0000-0000-0000-000000000001",
        "state_code": "JH",
        "state_name": "Jharkhand",
        "district_name": "Dhanbad",
        "latitude": 23.83,
        "longitude": 86.52,
        "elevation_m": 230,
        "area_sq_km": 450
    },
    {
        "id": "c0000092-0000-0000-0000-000000000001",
        "name": "Baghmara",
        "name_local": "Baghmara",
        "code": "JH-DHA-BAG",
        "level": "block",
        "parent_id": "b0000045-0000-0000-0000-000000000001",
        "state_code": "JH",
        "state_name": "Jharkhand",
        "district_name": "Dhanbad",
        "latitude": 23.78,
        "longitude": 86.2,
        "elevation_m": 220,
        "area_sq_km": 450
    },
    {
        "id": "b0000046-0000-0000-0000-000000000001",
        "name": "Wayanad",
        "name_local": "വയനാട്",
        "code": "KL-WAY",
        "level": "district",
        "parent_id": "a0000016-0000-0000-0000-000000000001",
        "state_code": "KL",
        "state_name": "Kerala",
        "district_name": None,
        "latitude": 11.6854,
        "longitude": 76.132,
        "elevation_m": 700,
        "area_sq_km": 19432
    },
    {
        "id": "c0000093-0000-0000-0000-000000000001",
        "name": "Mananthavady",
        "name_local": "Mananthavady",
        "code": "KL-WAY-MAN",
        "level": "block",
        "parent_id": "b0000046-0000-0000-0000-000000000001",
        "state_code": "KL",
        "state_name": "Kerala",
        "district_name": "Wayanad",
        "latitude": 11.8,
        "longitude": 76.0,
        "elevation_m": 760,
        "area_sq_km": 450
    },
    {
        "id": "c0000094-0000-0000-0000-000000000001",
        "name": "Sulthan Bathery",
        "name_local": "Sulthan Bathery",
        "code": "KL-WAY-SUL",
        "level": "block",
        "parent_id": "b0000046-0000-0000-0000-000000000001",
        "state_code": "KL",
        "state_name": "Kerala",
        "district_name": "Wayanad",
        "latitude": 11.66,
        "longitude": 76.26,
        "elevation_m": 930,
        "area_sq_km": 450
    },
    {
        "id": "b0000047-0000-0000-0000-000000000001",
        "name": "Palakkad",
        "name_local": "പാലക്കാട്",
        "code": "KL-PAL",
        "level": "district",
        "parent_id": "a0000016-0000-0000-0000-000000000001",
        "state_code": "KL",
        "state_name": "Kerala",
        "district_name": None,
        "latitude": 10.7867,
        "longitude": 76.6548,
        "elevation_m": 84,
        "area_sq_km": 19432
    },
    {
        "id": "c0000095-0000-0000-0000-000000000001",
        "name": "Chittur",
        "name_local": "Chittur",
        "code": "KL-PAL-CHI",
        "level": "block",
        "parent_id": "b0000047-0000-0000-0000-000000000001",
        "state_code": "KL",
        "state_name": "Kerala",
        "district_name": "Palakkad",
        "latitude": 10.7,
        "longitude": 76.72,
        "elevation_m": 110,
        "area_sq_km": 450
    },
    {
        "id": "c0000096-0000-0000-0000-000000000001",
        "name": "Alathur",
        "name_local": "Alathur",
        "code": "KL-PAL-ALA",
        "level": "block",
        "parent_id": "b0000047-0000-0000-0000-000000000001",
        "state_code": "KL",
        "state_name": "Kerala",
        "district_name": "Palakkad",
        "latitude": 10.64,
        "longitude": 76.54,
        "elevation_m": 78,
        "area_sq_km": 450
    },
    {
        "id": "b0000048-0000-0000-0000-000000000001",
        "name": "Imphal West",
        "name_local": "ইম্ফাল ৱেষ্ট",
        "code": "MN-IMP",
        "level": "district",
        "parent_id": "a0000017-0000-0000-0000-000000000001",
        "state_code": "MN",
        "state_name": "Manipur",
        "district_name": None,
        "latitude": 24.817,
        "longitude": 93.9368,
        "elevation_m": 786,
        "area_sq_km": 22327
    },
    {
        "id": "c0000097-0000-0000-0000-000000000001",
        "name": "Lamphelpat",
        "name_local": "Lamphelpat",
        "code": "MN-IMP-LAM",
        "level": "block",
        "parent_id": "b0000048-0000-0000-0000-000000000001",
        "state_code": "MN",
        "state_name": "Manipur",
        "district_name": "Imphal West",
        "latitude": 24.82,
        "longitude": 93.92,
        "elevation_m": 785,
        "area_sq_km": 450
    },
    {
        "id": "c0000098-0000-0000-0000-000000000001",
        "name": "Wangoi",
        "name_local": "Wangoi",
        "code": "MN-IMP-WAN",
        "level": "block",
        "parent_id": "b0000048-0000-0000-0000-000000000001",
        "state_code": "MN",
        "state_name": "Manipur",
        "district_name": "Imphal West",
        "latitude": 24.68,
        "longitude": 93.91,
        "elevation_m": 780,
        "area_sq_km": 450
    },
    {
        "id": "b0000049-0000-0000-0000-000000000001",
        "name": "East Khasi Hills",
        "name_local": "ইষ্ট খাছী হিলচ",
        "code": "ML-EKH",
        "level": "district",
        "parent_id": "a0000018-0000-0000-0000-000000000001",
        "state_code": "ML",
        "state_name": "Meghalaya",
        "district_name": None,
        "latitude": 25.5788,
        "longitude": 91.8933,
        "elevation_m": 1525,
        "area_sq_km": 22429
    },
    {
        "id": "c0000099-0000-0000-0000-000000000001",
        "name": "Mawphlang",
        "name_local": "Mawphlang",
        "code": "ML-EKH-MAW",
        "level": "block",
        "parent_id": "b0000049-0000-0000-0000-000000000001",
        "state_code": "ML",
        "state_name": "Meghalaya",
        "district_name": "East Khasi Hills",
        "latitude": 25.45,
        "longitude": 91.76,
        "elevation_m": 1820,
        "area_sq_km": 450
    },
    {
        "id": "c0000100-0000-0000-0000-000000000001",
        "name": "Sohra (Cherrapunji)",
        "name_local": "Sohra (Cherrapunji)",
        "code": "ML-EKH-SOH",
        "level": "block",
        "parent_id": "b0000049-0000-0000-0000-000000000001",
        "state_code": "ML",
        "state_name": "Meghalaya",
        "district_name": "East Khasi Hills",
        "latitude": 25.27,
        "longitude": 91.73,
        "elevation_m": 1430,
        "area_sq_km": 450
    },
    {
        "id": "b0000050-0000-0000-0000-000000000001",
        "name": "Aizawl",
        "name_local": "আইজল",
        "code": "MZ-AIZ",
        "level": "district",
        "parent_id": "a0000019-0000-0000-0000-000000000001",
        "state_code": "MZ",
        "state_name": "Mizoram",
        "district_name": None,
        "latitude": 23.7271,
        "longitude": 92.7176,
        "elevation_m": 1132,
        "area_sq_km": 21081
    },
    {
        "id": "c0000101-0000-0000-0000-000000000001",
        "name": "Tlangnuam",
        "name_local": "Tlangnuam",
        "code": "MZ-AIZ-TLA",
        "level": "block",
        "parent_id": "b0000050-0000-0000-0000-000000000001",
        "state_code": "MZ",
        "state_name": "Mizoram",
        "district_name": "Aizawl",
        "latitude": 23.68,
        "longitude": 92.72,
        "elevation_m": 1100,
        "area_sq_km": 450
    },
    {
        "id": "c0000102-0000-0000-0000-000000000001",
        "name": "Darlawn",
        "name_local": "Darlawn",
        "code": "MZ-AIZ-DAR",
        "level": "block",
        "parent_id": "b0000050-0000-0000-0000-000000000001",
        "state_code": "MZ",
        "state_name": "Mizoram",
        "district_name": "Aizawl",
        "latitude": 23.99,
        "longitude": 92.91,
        "elevation_m": 920,
        "area_sq_km": 450
    },
    {
        "id": "b0000051-0000-0000-0000-000000000001",
        "name": "Kohima",
        "name_local": "कोहिमा",
        "code": "NL-KOH",
        "level": "district",
        "parent_id": "a0000020-0000-0000-0000-000000000001",
        "state_code": "NL",
        "state_name": "Nagaland",
        "district_name": None,
        "latitude": 25.6751,
        "longitude": 94.1086,
        "elevation_m": 1444,
        "area_sq_km": 16579
    },
    {
        "id": "c0000103-0000-0000-0000-000000000001",
        "name": "Chiephobozou",
        "name_local": "Chiephobozou",
        "code": "NL-KOH-CHI",
        "level": "block",
        "parent_id": "b0000051-0000-0000-0000-000000000001",
        "state_code": "NL",
        "state_name": "Nagaland",
        "district_name": "Kohima",
        "latitude": 25.8,
        "longitude": 94.13,
        "elevation_m": 1380,
        "area_sq_km": 450
    },
    {
        "id": "c0000104-0000-0000-0000-000000000001",
        "name": "Jakhama",
        "name_local": "Jakhama",
        "code": "NL-KOH-JAK",
        "level": "block",
        "parent_id": "b0000051-0000-0000-0000-000000000001",
        "state_code": "NL",
        "state_name": "Nagaland",
        "district_name": "Kohima",
        "latitude": 25.57,
        "longitude": 94.15,
        "elevation_m": 1490,
        "area_sq_km": 450
    },
    {
        "id": "b0000052-0000-0000-0000-000000000001",
        "name": "Cuttack",
        "name_local": "କଟକ",
        "code": "OD-CUT",
        "level": "district",
        "parent_id": "a0000021-0000-0000-0000-000000000001",
        "state_code": "OD",
        "state_name": "Odisha",
        "district_name": None,
        "latitude": 20.4625,
        "longitude": 85.8828,
        "elevation_m": 36,
        "area_sq_km": 77854
    },
    {
        "id": "c0000105-0000-0000-0000-000000000001",
        "name": "Athagarh",
        "name_local": "Athagarh",
        "code": "OD-CUT-ATH",
        "level": "block",
        "parent_id": "b0000052-0000-0000-0000-000000000001",
        "state_code": "OD",
        "state_name": "Odisha",
        "district_name": "Cuttack",
        "latitude": 20.52,
        "longitude": 85.63,
        "elevation_m": 65,
        "area_sq_km": 450
    },
    {
        "id": "c0000106-0000-0000-0000-000000000001",
        "name": "Salepur",
        "name_local": "Salepur",
        "code": "OD-CUT-SAL",
        "level": "block",
        "parent_id": "b0000052-0000-0000-0000-000000000001",
        "state_code": "OD",
        "state_name": "Odisha",
        "district_name": "Cuttack",
        "latitude": 20.48,
        "longitude": 86.01,
        "elevation_m": 28,
        "area_sq_km": 450
    },
    {
        "id": "b0000053-0000-0000-0000-000000000001",
        "name": "Sambalpur",
        "name_local": "ସମ୍ବଲପୁର",
        "code": "OD-SAM",
        "level": "district",
        "parent_id": "a0000021-0000-0000-0000-000000000001",
        "state_code": "OD",
        "state_name": "Odisha",
        "district_name": None,
        "latitude": 21.4669,
        "longitude": 83.9812,
        "elevation_m": 135,
        "area_sq_km": 77854
    },
    {
        "id": "c0000107-0000-0000-0000-000000000001",
        "name": "Rengali",
        "name_local": "Rengali",
        "code": "OD-SAM-REN",
        "level": "block",
        "parent_id": "b0000053-0000-0000-0000-000000000001",
        "state_code": "OD",
        "state_name": "Odisha",
        "district_name": "Sambalpur",
        "latitude": 21.63,
        "longitude": 84.03,
        "elevation_m": 150,
        "area_sq_km": 450
    },
    {
        "id": "c0000108-0000-0000-0000-000000000001",
        "name": "Kuchinda",
        "name_local": "Kuchinda",
        "code": "OD-SAM-KUC",
        "level": "block",
        "parent_id": "b0000053-0000-0000-0000-000000000001",
        "state_code": "OD",
        "state_name": "Odisha",
        "district_name": "Sambalpur",
        "latitude": 22.02,
        "longitude": 84.35,
        "elevation_m": 210,
        "area_sq_km": 450
    },
    {
        "id": "b0000054-0000-0000-0000-000000000001",
        "name": "Jaipur",
        "name_local": "जयपुर",
        "code": "RJ-JAI",
        "level": "district",
        "parent_id": "a0000022-0000-0000-0000-000000000001",
        "state_code": "RJ",
        "state_name": "Rajasthan",
        "district_name": None,
        "latitude": 26.9124,
        "longitude": 75.7873,
        "elevation_m": 431,
        "area_sq_km": 171120
    },
    {
        "id": "c0000109-0000-0000-0000-000000000001",
        "name": "Sanganer",
        "name_local": "Sanganer",
        "code": "RJ-JAI-SAN",
        "level": "block",
        "parent_id": "b0000054-0000-0000-0000-000000000001",
        "state_code": "RJ",
        "state_name": "Rajasthan",
        "district_name": "Jaipur",
        "latitude": 26.82,
        "longitude": 75.77,
        "elevation_m": 420,
        "area_sq_km": 450
    },
    {
        "id": "c0000110-0000-0000-0000-000000000001",
        "name": "Chomu",
        "name_local": "Chomu",
        "code": "RJ-JAI-CHO",
        "level": "block",
        "parent_id": "b0000054-0000-0000-0000-000000000001",
        "state_code": "RJ",
        "state_name": "Rajasthan",
        "district_name": "Jaipur",
        "latitude": 27.17,
        "longitude": 75.72,
        "elevation_m": 440,
        "area_sq_km": 450
    },
    {
        "id": "b0000055-0000-0000-0000-000000000001",
        "name": "Kota",
        "name_local": "कोटा",
        "code": "RJ-KOT",
        "level": "district",
        "parent_id": "a0000022-0000-0000-0000-000000000001",
        "state_code": "RJ",
        "state_name": "Rajasthan",
        "district_name": None,
        "latitude": 25.2138,
        "longitude": 75.8648,
        "elevation_m": 271,
        "area_sq_km": 171120
    },
    {
        "id": "c0000111-0000-0000-0000-000000000001",
        "name": "Sangod",
        "name_local": "Sangod",
        "code": "RJ-KOT-SNG",
        "level": "block",
        "parent_id": "b0000055-0000-0000-0000-000000000001",
        "state_code": "RJ",
        "state_name": "Rajasthan",
        "district_name": "Kota",
        "latitude": 24.92,
        "longitude": 76.28,
        "elevation_m": 265,
        "area_sq_km": 450
    },
    {
        "id": "c0000112-0000-0000-0000-000000000001",
        "name": "Ladpura",
        "name_local": "Ladpura",
        "code": "RJ-KOT-LAD",
        "level": "block",
        "parent_id": "b0000055-0000-0000-0000-000000000001",
        "state_code": "RJ",
        "state_name": "Rajasthan",
        "district_name": "Kota",
        "latitude": 25.18,
        "longitude": 75.83,
        "elevation_m": 270,
        "area_sq_km": 450
    },
    {
        "id": "b0000056-0000-0000-0000-000000000001",
        "name": "East Sikkim",
        "name_local": "पूर्वी सिक्किम",
        "code": "SK-EAS",
        "level": "district",
        "parent_id": "a0000023-0000-0000-0000-000000000001",
        "state_code": "SK",
        "state_name": "Sikkim",
        "district_name": None,
        "latitude": 27.3389,
        "longitude": 88.6065,
        "elevation_m": 1650,
        "area_sq_km": 7096
    },
    {
        "id": "c0000113-0000-0000-0000-000000000001",
        "name": "Gangtok",
        "name_local": "Gangtok",
        "code": "SK-EAS-GAN",
        "level": "block",
        "parent_id": "b0000056-0000-0000-0000-000000000001",
        "state_code": "SK",
        "state_name": "Sikkim",
        "district_name": "East Sikkim",
        "latitude": 27.3314,
        "longitude": 88.6138,
        "elevation_m": 1650,
        "area_sq_km": 450
    },
    {
        "id": "c0000114-0000-0000-0000-000000000001",
        "name": "Pakyong",
        "name_local": "Pakyong",
        "code": "SK-EAS-PAK",
        "level": "block",
        "parent_id": "b0000056-0000-0000-0000-000000000001",
        "state_code": "SK",
        "state_name": "Sikkim",
        "district_name": "East Sikkim",
        "latitude": 27.23,
        "longitude": 88.59,
        "elevation_m": 1120,
        "area_sq_km": 450
    },
    {
        "id": "b0000057-0000-0000-0000-000000000001",
        "name": "Thanjavur",
        "name_local": "தஞ்சாவூர்",
        "code": "TN-THA",
        "level": "district",
        "parent_id": "a0000024-0000-0000-0000-000000000001",
        "state_code": "TN",
        "state_name": "Tamil Nadu",
        "district_name": None,
        "latitude": 10.787,
        "longitude": 79.1378,
        "elevation_m": 57,
        "area_sq_km": 65029
    },
    {
        "id": "c0000115-0000-0000-0000-000000000001",
        "name": "Kumbakonam",
        "name_local": "Kumbakonam",
        "code": "TN-THA-KUM",
        "level": "block",
        "parent_id": "b0000057-0000-0000-0000-000000000001",
        "state_code": "TN",
        "state_name": "Tamil Nadu",
        "district_name": "Thanjavur",
        "latitude": 10.96,
        "longitude": 79.38,
        "elevation_m": 24,
        "area_sq_km": 450
    },
    {
        "id": "c0000116-0000-0000-0000-000000000001",
        "name": "Papanasam",
        "name_local": "Papanasam",
        "code": "TN-THA-PAP",
        "level": "block",
        "parent_id": "b0000057-0000-0000-0000-000000000001",
        "state_code": "TN",
        "state_name": "Tamil Nadu",
        "district_name": "Thanjavur",
        "latitude": 10.92,
        "longitude": 79.28,
        "elevation_m": 32,
        "area_sq_km": 450
    },
    {
        "id": "b0000058-0000-0000-0000-000000000001",
        "name": "Coimbatore",
        "name_local": "கோயம்புத்தூர்",
        "code": "TN-COI",
        "level": "district",
        "parent_id": "a0000024-0000-0000-0000-000000000001",
        "state_code": "TN",
        "state_name": "Tamil Nadu",
        "district_name": None,
        "latitude": 11.0168,
        "longitude": 76.9558,
        "elevation_m": 411,
        "area_sq_km": 65029
    },
    {
        "id": "c0000117-0000-0000-0000-000000000001",
        "name": "Pollachi",
        "name_local": "Pollachi",
        "code": "TN-COI-POL",
        "level": "block",
        "parent_id": "b0000058-0000-0000-0000-000000000001",
        "state_code": "TN",
        "state_name": "Tamil Nadu",
        "district_name": "Coimbatore",
        "latitude": 10.66,
        "longitude": 77.01,
        "elevation_m": 293,
        "area_sq_km": 450
    },
    {
        "id": "c0000118-0000-0000-0000-000000000001",
        "name": "Sulur",
        "name_local": "Sulur",
        "code": "TN-COI-SUL",
        "level": "block",
        "parent_id": "b0000058-0000-0000-0000-000000000001",
        "state_code": "TN",
        "state_name": "Tamil Nadu",
        "district_name": "Coimbatore",
        "latitude": 11.02,
        "longitude": 77.12,
        "elevation_m": 340,
        "area_sq_km": 450
    },
    {
        "id": "b0000059-0000-0000-0000-000000000001",
        "name": "Warangal",
        "name_local": "వరంగల్",
        "code": "TS-WAR",
        "level": "district",
        "parent_id": "a0000025-0000-0000-0000-000000000001",
        "state_code": "TS",
        "state_name": "Telangana",
        "district_name": None,
        "latitude": 17.9689,
        "longitude": 79.5941,
        "elevation_m": 266,
        "area_sq_km": 56038
    },
    {
        "id": "c0000119-0000-0000-0000-000000000001",
        "name": "Wardhannapet",
        "name_local": "Wardhannapet",
        "code": "TS-WAR-WRD",
        "level": "block",
        "parent_id": "b0000059-0000-0000-0000-000000000001",
        "state_code": "TS",
        "state_name": "Telangana",
        "district_name": "Warangal",
        "latitude": 17.77,
        "longitude": 79.62,
        "elevation_m": 255,
        "area_sq_km": 450
    },
    {
        "id": "c0000120-0000-0000-0000-000000000001",
        "name": "Parkal",
        "name_local": "Parkal",
        "code": "TS-WAR-PAR",
        "level": "block",
        "parent_id": "b0000059-0000-0000-0000-000000000001",
        "state_code": "TS",
        "state_name": "Telangana",
        "district_name": "Warangal",
        "latitude": 18.2,
        "longitude": 79.71,
        "elevation_m": 240,
        "area_sq_km": 450
    },
    {
        "id": "b0000060-0000-0000-0000-000000000001",
        "name": "Nizamabad",
        "name_local": "నిజామాబాద్",
        "code": "TS-NIZ",
        "level": "district",
        "parent_id": "a0000025-0000-0000-0000-000000000001",
        "state_code": "TS",
        "state_name": "Telangana",
        "district_name": None,
        "latitude": 18.6725,
        "longitude": 78.0941,
        "elevation_m": 395,
        "area_sq_km": 56038
    },
    {
        "id": "c0000121-0000-0000-0000-000000000001",
        "name": "Armoor",
        "name_local": "Armoor",
        "code": "TS-NIZ-ARM",
        "level": "block",
        "parent_id": "b0000060-0000-0000-0000-000000000001",
        "state_code": "TS",
        "state_name": "Telangana",
        "district_name": "Nizamabad",
        "latitude": 18.79,
        "longitude": 78.29,
        "elevation_m": 375,
        "area_sq_km": 450
    },
    {
        "id": "c0000122-0000-0000-0000-000000000001",
        "name": "Bodhan",
        "name_local": "Bodhan",
        "code": "TS-NIZ-BOD",
        "level": "block",
        "parent_id": "b0000060-0000-0000-0000-000000000001",
        "state_code": "TS",
        "state_name": "Telangana",
        "district_name": "Nizamabad",
        "latitude": 18.66,
        "longitude": 77.88,
        "elevation_m": 357,
        "area_sq_km": 450
    },
    {
        "id": "b0000061-0000-0000-0000-000000000001",
        "name": "West Tripura",
        "name_local": "পশ্চিম ত্রিপুরা",
        "code": "TR-WES",
        "level": "district",
        "parent_id": "a0000026-0000-0000-0000-000000000001",
        "state_code": "TR",
        "state_name": "Tripura",
        "district_name": None,
        "latitude": 23.8315,
        "longitude": 91.2868,
        "elevation_m": 25,
        "area_sq_km": 10491
    },
    {
        "id": "c0000123-0000-0000-0000-000000000001",
        "name": "Jirania",
        "name_local": "Jirania",
        "code": "TR-WES-JIR",
        "level": "block",
        "parent_id": "b0000061-0000-0000-0000-000000000001",
        "state_code": "TR",
        "state_name": "Tripura",
        "district_name": "West Tripura",
        "latitude": 23.82,
        "longitude": 91.43,
        "elevation_m": 30,
        "area_sq_km": 450
    },
    {
        "id": "c0000124-0000-0000-0000-000000000001",
        "name": "Mohanpur",
        "name_local": "Mohanpur",
        "code": "TR-WES-MOH",
        "level": "block",
        "parent_id": "b0000061-0000-0000-0000-000000000001",
        "state_code": "TR",
        "state_name": "Tripura",
        "district_name": "West Tripura",
        "latitude": 23.97,
        "longitude": 91.37,
        "elevation_m": 28,
        "area_sq_km": 450
    },
    {
        "id": "b0000062-0000-0000-0000-000000000001",
        "name": "Dehradun",
        "name_local": "देहरादून",
        "code": "UK-DEH",
        "level": "district",
        "parent_id": "a0000027-0000-0000-0000-000000000001",
        "state_code": "UK",
        "state_name": "Uttarakhand",
        "district_name": None,
        "latitude": 30.3165,
        "longitude": 78.0322,
        "elevation_m": 435,
        "area_sq_km": 26742
    },
    {
        "id": "c0000125-0000-0000-0000-000000000001",
        "name": "Rishikesh",
        "name_local": "Rishikesh",
        "code": "UK-DEH-RIS",
        "level": "block",
        "parent_id": "b0000062-0000-0000-0000-000000000001",
        "state_code": "UK",
        "state_name": "Uttarakhand",
        "district_name": "Dehradun",
        "latitude": 30.0869,
        "longitude": 78.2676,
        "elevation_m": 372,
        "area_sq_km": 450
    },
    {
        "id": "c0000126-0000-0000-0000-000000000001",
        "name": "Vikasnagar",
        "name_local": "Vikasnagar",
        "code": "UK-DEH-VIK",
        "level": "block",
        "parent_id": "b0000062-0000-0000-0000-000000000001",
        "state_code": "UK",
        "state_name": "Uttarakhand",
        "district_name": "Dehradun",
        "latitude": 30.49,
        "longitude": 77.77,
        "elevation_m": 452,
        "area_sq_km": 450
    },
    {
        "id": "b0000063-0000-0000-0000-000000000001",
        "name": "Haridwar",
        "name_local": "हरिद्वार",
        "code": "UK-HAR",
        "level": "district",
        "parent_id": "a0000027-0000-0000-0000-000000000001",
        "state_code": "UK",
        "state_name": "Uttarakhand",
        "district_name": None,
        "latitude": 29.9457,
        "longitude": 78.1642,
        "elevation_m": 314,
        "area_sq_km": 26742
    },
    {
        "id": "c0000127-0000-0000-0000-000000000001",
        "name": "Roorkee",
        "name_local": "Roorkee",
        "code": "UK-HAR-ROO",
        "level": "block",
        "parent_id": "b0000063-0000-0000-0000-000000000001",
        "state_code": "UK",
        "state_name": "Uttarakhand",
        "district_name": "Haridwar",
        "latitude": 29.8543,
        "longitude": 77.888,
        "elevation_m": 268,
        "area_sq_km": 450
    },
    {
        "id": "c0000128-0000-0000-0000-000000000001",
        "name": "Laksar",
        "name_local": "Laksar",
        "code": "UK-HAR-LAK",
        "level": "block",
        "parent_id": "b0000063-0000-0000-0000-000000000001",
        "state_code": "UK",
        "state_name": "Uttarakhand",
        "district_name": "Haridwar",
        "latitude": 29.75,
        "longitude": 78.03,
        "elevation_m": 245,
        "area_sq_km": 450
    },
    {
        "id": "b0000064-0000-0000-0000-000000000001",
        "name": "Purba Bardhaman",
        "name_local": "পূর্ব বর্ধমান",
        "code": "WB-BUR",
        "level": "district",
        "parent_id": "a0000028-0000-0000-0000-000000000001",
        "state_code": "WB",
        "state_name": "West Bengal",
        "district_name": None,
        "latitude": 23.2324,
        "longitude": 87.8615,
        "elevation_m": 35,
        "area_sq_km": 44376
    },
    {
        "id": "c0000129-0000-0000-0000-000000000001",
        "name": "Katwa",
        "name_local": "Katwa",
        "code": "WB-BUR-KAT",
        "level": "block",
        "parent_id": "b0000064-0000-0000-0000-000000000001",
        "state_code": "WB",
        "state_name": "West Bengal",
        "district_name": "Purba Bardhaman",
        "latitude": 23.65,
        "longitude": 88.13,
        "elevation_m": 21,
        "area_sq_km": 450
    },
    {
        "id": "c0000130-0000-0000-0000-000000000001",
        "name": "Kalna",
        "name_local": "Kalna",
        "code": "WB-BUR-KAL",
        "level": "block",
        "parent_id": "b0000064-0000-0000-0000-000000000001",
        "state_code": "WB",
        "state_name": "West Bengal",
        "district_name": "Purba Bardhaman",
        "latitude": 23.22,
        "longitude": 88.37,
        "elevation_m": 18,
        "area_sq_km": 450
    },
    {
        "id": "b0000065-0000-0000-0000-000000000001",
        "name": "Nadia",
        "name_local": "নদিয়া",
        "code": "WB-NAD",
        "level": "district",
        "parent_id": "a0000028-0000-0000-0000-000000000001",
        "state_code": "WB",
        "state_name": "West Bengal",
        "district_name": None,
        "latitude": 23.471,
        "longitude": 88.5565,
        "elevation_m": 15,
        "area_sq_km": 44376
    },
    {
        "id": "c0000131-0000-0000-0000-000000000001",
        "name": "Ranaghat",
        "name_local": "Ranaghat",
        "code": "WB-NAD-RAN",
        "level": "block",
        "parent_id": "b0000065-0000-0000-0000-000000000001",
        "state_code": "WB",
        "state_name": "West Bengal",
        "district_name": "Nadia",
        "latitude": 23.18,
        "longitude": 88.58,
        "elevation_m": 11,
        "area_sq_km": 450
    },
    {
        "id": "c0000132-0000-0000-0000-000000000001",
        "name": "Krishnanagar",
        "name_local": "Krishnanagar",
        "code": "WB-NAD-KRI",
        "level": "block",
        "parent_id": "b0000065-0000-0000-0000-000000000001",
        "state_code": "WB",
        "state_name": "West Bengal",
        "district_name": "Nadia",
        "latitude": 23.4,
        "longitude": 88.5,
        "elevation_m": 14,
        "area_sq_km": 450
    },
    {
        "id": "b0000066-0000-0000-0000-000000000001",
        "name": "North Delhi",
        "name_local": "उत्तरी दिल्ली",
        "code": "DL-NDL",
        "level": "district",
        "parent_id": "a0000029-0000-0000-0000-000000000001",
        "state_code": "DL",
        "state_name": "Delhi (NCT)",
        "district_name": None,
        "latitude": 28.7495,
        "longitude": 77.1534,
        "elevation_m": 218,
        "area_sq_km": 1484
    },
    {
        "id": "c0000133-0000-0000-0000-000000000001",
        "name": "Alipur",
        "name_local": "Alipur",
        "code": "DL-NDL-ALI",
        "level": "block",
        "parent_id": "b0000066-0000-0000-0000-000000000001",
        "state_code": "DL",
        "state_name": "Delhi (NCT)",
        "district_name": "North Delhi",
        "latitude": 28.79,
        "longitude": 77.13,
        "elevation_m": 216,
        "area_sq_km": 450
    },
    {
        "id": "c0000134-0000-0000-0000-000000000001",
        "name": "Narela",
        "name_local": "Narela",
        "code": "DL-NDL-NAR",
        "level": "block",
        "parent_id": "b0000066-0000-0000-0000-000000000001",
        "state_code": "DL",
        "state_name": "Delhi (NCT)",
        "district_name": "North Delhi",
        "latitude": 28.85,
        "longitude": 77.09,
        "elevation_m": 219,
        "area_sq_km": 450
    },
    {
        "id": "b0000067-0000-0000-0000-000000000001",
        "name": "Srinagar",
        "name_local": "سرینگر",
        "code": "JK-SRI",
        "level": "district",
        "parent_id": "a0000030-0000-0000-0000-000000000001",
        "state_code": "JK",
        "state_name": "Jammu & Kashmir",
        "district_name": None,
        "latitude": 34.0837,
        "longitude": 74.7973,
        "elevation_m": 1585,
        "area_sq_km": 21120
    },
    {
        "id": "c0000135-0000-0000-0000-000000000001",
        "name": "Hazratbal",
        "name_local": "Hazratbal",
        "code": "JK-SRI-HAZ",
        "level": "block",
        "parent_id": "b0000067-0000-0000-0000-000000000001",
        "state_code": "JK",
        "state_name": "Jammu & Kashmir",
        "district_name": "Srinagar",
        "latitude": 34.12,
        "longitude": 74.84,
        "elevation_m": 1590,
        "area_sq_km": 450
    },
    {
        "id": "c0000136-0000-0000-0000-000000000001",
        "name": "Eidgah",
        "name_local": "Eidgah",
        "code": "JK-SRI-EID",
        "level": "block",
        "parent_id": "b0000067-0000-0000-0000-000000000001",
        "state_code": "JK",
        "state_name": "Jammu & Kashmir",
        "district_name": "Srinagar",
        "latitude": 34.1,
        "longitude": 74.79,
        "elevation_m": 1580,
        "area_sq_km": 450
    },
    {
        "id": "b0000068-0000-0000-0000-000000000001",
        "name": "Jammu",
        "name_local": "جموں",
        "code": "JK-JAM",
        "level": "district",
        "parent_id": "a0000030-0000-0000-0000-000000000001",
        "state_code": "JK",
        "state_name": "Jammu & Kashmir",
        "district_name": None,
        "latitude": 32.7266,
        "longitude": 74.857,
        "elevation_m": 327,
        "area_sq_km": 21120
    },
    {
        "id": "c0000137-0000-0000-0000-000000000001",
        "name": "R.S. Pura",
        "name_local": "R.S. Pura",
        "code": "JK-JAM-RSP",
        "level": "block",
        "parent_id": "b0000068-0000-0000-0000-000000000001",
        "state_code": "JK",
        "state_name": "Jammu & Kashmir",
        "district_name": "Jammu",
        "latitude": 32.63,
        "longitude": 74.73,
        "elevation_m": 290,
        "area_sq_km": 450
    },
    {
        "id": "c0000138-0000-0000-0000-000000000001",
        "name": "Akhnoor",
        "name_local": "Akhnoor",
        "code": "JK-JAM-AKH",
        "level": "block",
        "parent_id": "b0000068-0000-0000-0000-000000000001",
        "state_code": "JK",
        "state_name": "Jammu & Kashmir",
        "district_name": "Jammu",
        "latitude": 32.89,
        "longitude": 74.73,
        "elevation_m": 305,
        "area_sq_km": 450
    }
]


DISTRICT_BOUNDS_MAP = {
    "MH-PUN": [
        [
            17.863,
            73.5
        ],
        [
            19.4579,
            75.3737
        ]
    ],
    "MH-NAG": [
        [
            20.8958,
            78.7
        ],
        [
            21.48,
            79.55
        ]
    ],
    "MH-NAS": [
        [
            19.44,
            73.21
        ],
        [
            20.8,
            74.88
        ]
    ],
    "MH-AUR": [
        [
            19.23,
            74.66
        ],
        [
            20.1262,
            75.73
        ]
    ],
    "MH-KOL": [
        [
            16.43,
            73.87
        ],
        [
            17.0,
            74.8
        ]
    ],
    "MH-SOL": [
        [
            17.4099,
            74.97
        ],
        [
            18.48,
            76.2564
        ]
    ],
    "MH-SAT": [
        [
            17.03,
            73.54
        ],
        [
            18.2,
            74.55
        ]
    ],
    "MH-AHM": [
        [
            18.8448,
            73.86
        ],
        [
            19.87,
            75.098
        ]
    ],
    "KA-BEL": [
        [
            15.5997,
            74.1477
        ],
        [
            16.68,
            75.17
        ]
    ],
    "KA-DHA": [
        [
            15.1147,
            74.63
        ],
        [
            15.73,
            75.474
        ]
    ],
    "KA-RAI": [
        [
            15.52,
            76.41
        ],
        [
            16.4576,
            77.6963
        ]
    ],
    "KA-BLR": [
        [
            12.848,
            77.041
        ],
        [
            13.4983,
            78.0626
        ]
    ],
    "GJ-AHM": [
        [
            22.47,
            72.03
        ],
        [
            23.2725,
            72.9214
        ]
    ],
    "GJ-RAJ": [
        [
            21.71,
            70.45
        ],
        [
            22.5539,
            71.55
        ]
    ],
    "GJ-AND": [
        [
            22.16,
            72.45
        ],
        [
            22.8145,
            73.2789
        ]
    ],
    "GJ-SUR": [
        [
            20.87,
            72.4
        ],
        [
            21.58,
            73.46
        ]
    ],
    "MP-IND": [
        [
            22.3,
            75.2
        ],
        [
            23.1,
            76.2077
        ]
    ],
    "MP-UJJ": [
        [
            22.76,
            75.03
        ],
        [
            23.7,
            76.1385
        ]
    ],
    "MP-BHO": [
        [
            22.93,
            76.93
        ],
        [
            23.88,
            77.78
        ]
    ],
    "MP-HOS": [
        [
            22.36,
            77.3789
        ],
        [
            23.01,
            78.7
        ]
    ],
    "PB-LUD": [
        [
            30.45,
            75.13
        ],
        [
            31.151,
            76.57
        ]
    ],
    "PB-AMR": [
        [
            31.384,
            74.41
        ],
        [
            32.09,
            75.31
        ]
    ],
    "PB-PAT": [
        [
            30.0898,
            75.8
        ],
        [
            30.73,
            76.95
        ]
    ],
    "PB-BAT": [
        [
            29.73,
            74.5955
        ],
        [
            30.52,
            75.59
        ]
    ],
    "UP-VAR": [
        [
            25.0676,
            82.5
        ],
        [
            25.77,
            83.4
        ]
    ],
    "UP-LUK": [
        [
            26.43,
            80.58
        ],
        [
            27.27,
            81.33
        ]
    ],
    "UP-GOR": [
        [
            26.5106,
            82.84
        ],
        [
            27.27,
            83.7232
        ]
    ],
    "UP-PRY": [
        [
            24.73,
            81.4963
        ],
        [
            25.8,
            82.43
        ]
    ],
    "AP-VIS": [
        [
            17.4368,
            82.6539
        ],
        [
            18.1406,
            83.8042
        ]
    ],
    "AP-GUN": [
        [
            15.993,
            80.0865
        ],
        [
            16.68,
            80.99
        ]
    ],
    "AR-PAP": [
        [
            26.8344,
            93.2553
        ],
        [
            27.3556,
            94.0434
        ]
    ],
    "AS-KAM": [
        [
            25.9982,
            91.1784
        ],
        [
            26.7173,
            91.9788
        ]
    ],
    "AS-DIB": [
        [
            26.9356,
            94.562
        ],
        [
            27.7228,
            95.6833
        ]
    ],
    "BR-PAT": [
        [
            25.32,
            84.69
        ],
        [
            25.88,
            85.4876
        ]
    ],
    "BR-MUZ": [
        [
            25.8709,
            84.92
        ],
        [
            26.45,
            85.7147
        ]
    ],
    "CG-RAI": [
        [
            20.8,
            81.2796
        ],
        [
            21.5014,
            82.31
        ]
    ],
    "CG-BIL": [
        [
            21.8297,
            81.51
        ],
        [
            22.54,
            82.4909
        ]
    ],
    "GA-NGO": [
        [
            15.24,
            73.46
        ],
        [
            15.84,
            74.21
        ]
    ],
    "GA-SGO": [
        [
            15.0236,
            73.608
        ],
        [
            15.65,
            74.37
        ]
    ],
    "HR-KAR": [
        [
            29.29,
            76.57
        ],
        [
            30.08,
            77.3405
        ]
    ],
    "HR-HIS": [
        [
            28.85,
            75.3717
        ],
        [
            29.63,
            76.31
        ]
    ],
    "HP-KAN": [
        [
            31.8498,
            75.9191
        ],
        [
            32.469,
            76.8863
        ]
    ],
    "HP-SHI": [
        [
            30.8548,
            76.8234
        ],
        [
            31.7,
            77.98
        ]
    ],
    "JH-RAN": [
        [
            23.0941,
            84.9596
        ],
        [
            23.73,
            85.83
        ]
    ],
    "JH-DHA": [
        [
            23.53,
            85.85
        ],
        [
            24.08,
            86.87
        ]
    ],
    "KL-WAY": [
        [
            11.41,
            75.65
        ],
        [
            12.05,
            76.61
        ]
    ],
    "KL-PAL": [
        [
            10.39,
            76.19
        ],
        [
            11.0367,
            77.07
        ]
    ],
    "MN-IMP": [
        [
            24.43,
            93.56
        ],
        [
            25.07,
            94.2868
        ]
    ],
    "ML-EKH": [
        [
            25.02,
            91.38
        ],
        [
            25.8288,
            92.2433
        ]
    ],
    "MZ-AIZ": [
        [
            23.43,
            92.3676
        ],
        [
            24.24,
            93.26
        ]
    ],
    "NL-KOH": [
        [
            25.32,
            93.7586
        ],
        [
            26.05,
            94.5
        ]
    ],
    "OD-CUT": [
        [
            20.2125,
            85.28
        ],
        [
            20.77,
            86.36
        ]
    ],
    "OD-SAM": [
        [
            21.2169,
            83.6312
        ],
        [
            22.27,
            84.7
        ]
    ],
    "RJ-JAI": [
        [
            26.57,
            75.37
        ],
        [
            27.42,
            76.1373
        ]
    ],
    "RJ-KOT": [
        [
            24.67,
            75.48
        ],
        [
            25.4638,
            76.63
        ]
    ],
    "SK-EAS": [
        [
            26.98,
            88.24
        ],
        [
            27.5889,
            88.9638
        ]
    ],
    "TN-THA": [
        [
            10.537,
            78.7878
        ],
        [
            11.21,
            79.73
        ]
    ],
    "TN-COI": [
        [
            10.41,
            76.6058
        ],
        [
            11.27,
            77.47
        ]
    ],
    "TS-WAR": [
        [
            17.52,
            79.2441
        ],
        [
            18.45,
            80.06
        ]
    ],
    "TS-NIZ": [
        [
            18.41,
            77.53
        ],
        [
            19.04,
            78.64
        ]
    ],
    "TR-WES": [
        [
            23.57,
            90.9368
        ],
        [
            24.22,
            91.78
        ]
    ],
    "UK-DEH": [
        [
            29.8369,
            77.42
        ],
        [
            30.74,
            78.6176
        ]
    ],
    "UK-HAR": [
        [
            29.5,
            77.538
        ],
        [
            30.1957,
            78.5142
        ]
    ],
    "WB-BUR": [
        [
            22.97,
            87.5115
        ],
        [
            23.9,
            88.72
        ]
    ],
    "WB-NAD": [
        [
            22.93,
            88.15
        ],
        [
            23.721,
            88.93
        ]
    ],
    "DL-NDL": [
        [
            28.4995,
            76.74
        ],
        [
            29.1,
            77.5034
        ]
    ],
    "JK-SRI": [
        [
            33.8337,
            74.44
        ],
        [
            34.37,
            75.19
        ]
    ],
    "JK-JAM": [
        [
            32.38,
            74.38
        ],
        [
            33.14,
            75.207
        ]
    ]
}


STATE_BOUNDS_MAP = {
    "MH": [
        [
            15.88,
            72.66
        ],
        [
            22.03,
            80.1
        ]
    ],
    "KA": [
        [
            12.298,
            73.69
        ],
        [
            17.23,
            78.6126
        ]
    ],
    "GJ": [
        [
            20.32,
            69.9
        ],
        [
            23.78,
            74.01
        ]
    ],
    "MP": [
        [
            21.75,
            74.48
        ],
        [
            24.43,
            79.5569
        ]
    ],
    "PB": [
        [
            29.18,
            73.86
        ],
        [
            32.64,
            77.5
        ]
    ],
    "UP": [
        [
            24.18,
            80.03
        ],
        [
            27.82,
            84.17
        ]
    ],
    "AP": [
        [
            15.1129,
            78.84
        ],
        [
            18.6906,
            84.3542
        ]
    ],
    "AR": [
        [
            26.2844,
            92.7053
        ],
        [
            29.018,
            95.6278
        ]
    ],
    "AS": [
        [
            25.4006,
            90.6284
        ],
        [
            28.0833,
            96.2333
        ]
    ],
    "BR": [
        [
            24.2961,
            84.14
        ],
        [
            27.0,
            86.2131
        ]
    ],
    "CG": [
        [
            20.25,
            80.84
        ],
        [
            23.09,
            82.92
        ]
    ],
    "GA": [
        [
            14.48,
            72.91
        ],
        [
            16.39,
            75.024
        ]
    ],
    "HR": [
        [
            28.2588,
            75.01
        ],
        [
            30.63,
            77.87
        ]
    ],
    "HP": [
        [
            30.3048,
            75.4234
        ],
        [
            33.019,
            78.53
        ]
    ],
    "JH": [
        [
            22.63,
            84.3799
        ],
        [
            24.63,
            87.42
        ]
    ],
    "KL": [
        [
            9.84,
            75.1
        ],
        [
            12.6,
            77.62
        ]
    ],
    "MN": [
        [
            23.8637,
            93.0063
        ],
        [
            25.62,
            94.82
        ]
    ],
    "ML": [
        [
            24.47,
            90.4662
        ],
        [
            26.267,
            92.66
        ]
    ],
    "MZ": [
        [
            22.3645,
            91.82
        ],
        [
            24.79,
            93.8376
        ]
    ],
    "NL": [
        [
            24.77,
            93.23
        ],
        [
            26.9584,
            95.4624
        ]
    ],
    "OD": [
        [
            19.68,
            83.13
        ],
        [
            22.82,
            86.91
        ]
    ],
    "RJ": [
        [
            24.12,
            73.3179
        ],
        [
            27.97,
            77.18
        ]
    ],
    "SK": [
        [
            26.43,
            87.6122
        ],
        [
            28.333,
            89.5138
        ]
    ],
    "TN": [
        [
            9.86,
            76.11
        ],
        [
            11.9271,
            80.28
        ]
    ],
    "TS": [
        [
            16.97,
            76.98
        ],
        [
            19.59,
            80.61
        ]
    ],
    "TR": [
        [
            23.02,
            90.47
        ],
        [
            24.77,
            92.8882
        ]
    ],
    "UK": [
        [
            28.95,
            76.87
        ],
        [
            31.29,
            79.9193
        ]
    ],
    "WB": [
        [
            22.1868,
            86.955
        ],
        [
            24.45,
            89.48
        ]
    ],
    "DL": [
        [
            27.9041,
            76.19
        ],
        [
            29.65,
            78.03
        ]
    ],
    "JK": [
        [
            31.83,
            73.83
        ],
        [
            34.92,
            77.4762
        ]
    ]
}


class LocationService:
    """In-memory location service for Pan-India MVP demo."""

    def __init__(self):
        self.locations: Dict[str, Dict] = {}
        for loc in DEMO_LOCATIONS:
            self.locations[loc["id"]] = loc

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

    def get_hierarchy_with_bounds(self, state_code: Optional[str] = None) -> Dict:
        """Returns nested hierarchy state -> districts -> blocks with bounding boxes."""
        states = [l for l in self.locations.values() if l["level"] == "state"]

        target_state = None
        if state_code:
            target_state = next((s for s in states if s["code"] == state_code), None)
        if not target_state:
            target_state = states[0] if states else None

        target_state_name = target_state["name"] if target_state else "Maharashtra"
        target_state_code = target_state["code"] if target_state else "MH"

        districts = [
            l for l in self.locations.values()
            if l["level"] == "district" and l.get("state_name") == target_state_name
        ]
        blocks = [
            l for l in self.locations.values()
            if l["level"] == "block" and l.get("state_name") == target_state_name
        ]

        enriched_districts = []
        for d in districts:
            d_copy = dict(d)
            bounds = DISTRICT_BOUNDS_MAP.get(d["code"])
            if not bounds:
                child_blocks = [b for b in blocks if b["parent_id"] == d["id"]]
                lats = [b["latitude"] for b in child_blocks] + [d["latitude"]]
                lngs = [b["longitude"] for b in child_blocks] + [d["longitude"]]
                bounds = [[min(lats) - 0.15, min(lngs) - 0.15], [max(lats) + 0.15, max(lngs) + 0.15]]
            d_copy["bounds"] = bounds
            enriched_districts.append(d_copy)

        return {
            "states": states,
            "state": target_state,
            "districts": enriched_districts,
            "blocks": blocks,
            "bounds": STATE_BOUNDS_MAP.get(target_state_code, [[15.6, 72.6], [22.0, 80.9]]),
        }


# Singleton
location_service = LocationService()
