"""
MonSense Location API Router
Endpoints for location hierarchy, search, and GeoJSON layers.
— Priya Nair (Data Engineering & Spatial Pipeline Lead)
— Siddharth Rao (GIS Vector Tile & Rendering Optimizer)
"""

from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from app.services.location_service import location_service

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/")
async def list_locations(
    level: Optional[str] = Query(default=None, regex="^(state|district|block|village|panchayat)$"),
    district_id: Optional[str] = None,
):
    """List all locations, optionally filtered by level or district."""
    if district_id:
        locations = location_service.get_children(district_id)
        if level:
            locations = [l for l in locations if l["level"] == level]
    elif level:
        locations = location_service.get_all(level=level)
    else:
        locations = location_service.get_all()

    return {
        "total": len(locations),
        "locations": locations,
    }


@router.get("/search")
async def search_locations(
    q: str = Query(min_length=2),
):
    """Search locations by name."""
    results = location_service.search(q)
    return {
        "query": q,
        "total": len(results),
        "results": results,
    }


@router.get("/hierarchy")
async def get_hierarchy():
    """Get full location hierarchy tree."""
    states = location_service.get_all(level="state")
    tree = []

    for state in states:
        state_node = {**state, "children": []}
        districts = location_service.get_children(state["id"])

        for district in districts:
            district_node = {**district, "children": []}
            blocks = location_service.get_children(district["id"])

            for block in blocks:
                block_node = {**block, "children": []}
                villages = location_service.get_children(block["id"])
                block_node["children"] = villages
                district_node["children"].append(block_node)

            state_node["children"].append(district_node)
        tree.append(state_node)

    return {"hierarchy": tree}


@router.get("/hierarchy-with-bounds")
async def get_hierarchy_with_bounds(state_code: Optional[str] = Query(default=None, description="State code filter like MH, KA, GJ, MP, PB, UP")):
    """Get full location hierarchy with bounding box coordinates for GIS maps."""
    return location_service.get_hierarchy_with_bounds(state_code=state_code)


@router.get("/districts")
async def list_districts(
    state_id: Optional[str] = None,
):
    """List all districts."""
    if state_id:
        districts = location_service.get_children(state_id)
    else:
        districts = location_service.get_all(level="district")
    return {"total": len(districts), "districts": districts}


@router.get("/blocks")
async def list_blocks(
    district_id: Optional[str] = None,
):
    """List all blocks."""
    blocks = location_service.get_blocks(district_id)
    return {"total": len(blocks), "blocks": blocks}


@router.get("/{location_id}")
async def get_location(location_id: str):
    """Get a specific location by ID."""
    location = location_service.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.get("/{location_id}/children")
async def get_children(location_id: str):
    """Get child locations."""
    children = location_service.get_children(location_id)
    return {"parent_id": location_id, "total": len(children), "children": children}
