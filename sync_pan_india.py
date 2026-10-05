import json
import uuid
import re

with open("pan_india.json", "r", encoding="utf-8") as f:
    pan_india = json.load(f)

# Build flattened locations list
demo_locations = []
district_bounds_map = {}
state_bounds_map = {}

state_id_map = {}
district_id_map = {}

# Keep stable UUID prefixes for MH, KA, GJ, MP, PB, UP
KNOWN_STATE_IDS = {
    "MH": "a0000001-0000-0000-0000-000000000001",
    "KA": "a0000002-0000-0000-0000-000000000001",
    "GJ": "a0000003-0000-0000-0000-000000000001",
    "MP": "a0000004-0000-0000-0000-000000000001",
    "PB": "a0000005-0000-0000-0000-000000000001",
    "UP": "a0000006-0000-0000-0000-000000000001",
}

# 1. Generate States
for i, s in enumerate(pan_india):
    scode = s["code"]
    sid = KNOWN_STATE_IDS.get(scode, f"a{i+1:07d}-0000-0000-0000-000000000001")
    state_id_map[scode] = sid
    demo_locations.append({
        "id": sid,
        "name": s["name"],
        "name_local": s["name_local"],
        "code": scode,
        "level": "state",
        "parent_id": None,
        "state_name": s["name"],
        "district_name": None,
        "latitude": s["lat"],
        "longitude": s["lon"],
        "elevation_m": s["elev"],
        "area_sq_km": s["area"],
    })

# 2. Generate Districts & Blocks
dist_counter = 1
block_counter = 1

for s in pan_india:
    scode = s["code"]
    sname = s["name"]
    sid = state_id_map[scode]
    state_lats = [s["lat"]]
    state_lngs = [s["lon"]]

    for d in s["districts"]:
        dcode = d["code"]
        did = f"b{dist_counter:07d}-0000-0000-0000-000000000001"
        dist_counter += 1
        district_id_map[dcode] = did

        demo_locations.append({
            "id": did,
            "name": d["name"],
            "name_local": d["name_local"],
            "code": dcode,
            "level": "district",
            "parent_id": sid,
            "state_code": scode,
            "state_name": sname,
            "district_name": None,
            "latitude": d["lat"],
            "longitude": d["lon"],
            "elevation_m": d["elev"],
            "area_sq_km": round(s["area"] / max(1, len(s["districts"]))),
        })

        dist_lats = [d["lat"]]
        dist_lngs = [d["lon"]]

        for b in d["blocks"]:
            bcode = b["code"]
            bid = f"c{block_counter:07d}-0000-0000-0000-000000000001"
            block_counter += 1

            demo_locations.append({
                "id": bid,
                "name": b["name"],
                "name_local": b["name"],
                "code": bcode,
                "level": "block",
                "parent_id": did,
                "state_code": scode,
                "state_name": sname,
                "district_name": d["name"],
                "latitude": b["lat"],
                "longitude": b["lon"],
                "elevation_m": b["elev"],
                "area_sq_km": 450,
            })

            dist_lats.append(b["lat"])
            dist_lngs.append(b["lon"])
            state_lats.append(b["lat"])
            state_lngs.append(b["lon"])

        # Compute District bounds
        min_lat, max_lat = min(dist_lats) - 0.25, max(dist_lats) + 0.25
        min_lng, max_lng = min(dist_lngs) - 0.35, max(dist_lngs) + 0.35
        district_bounds_map[dcode] = [
            [round(min_lat, 4), round(min_lng, 4)],
            [round(max_lat, 4), round(max_lng, 4)]
        ]

    # Compute State bounds
    min_lat, max_lat = min(state_lats) - 0.8, max(state_lats) + 0.8
    min_lng, max_lng = min(state_lngs) - 0.9, max(state_lngs) + 0.9
    state_bounds_map[scode] = [
        [round(min_lat, 4), round(min_lng, 4)],
        [round(max_lat, 4), round(max_lng, 4)]
    ]

print(f"Generated {len(demo_locations)} total locations across {len(pan_india)} states/UTs.")
print(f"Districts: {len(district_bounds_map)}, States bounds: {len(state_bounds_map)}")

# Save to intermediate JSON for inspection
with open("synced_locations.json", "w", encoding="utf-8") as f:
    json.dump({
        "demo_locations": demo_locations,
        "district_bounds": district_bounds_map,
        "state_bounds": state_bounds_map,
    }, f, ensure_ascii=False, indent=2)

print("Saved synced_locations.json successfully.")
