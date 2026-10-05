/**
 * MonSense Risk Map Component
 * Interactive Leaflet.js GIS map with CartoDB Voyager pastel basemap,
 * multi-vertex organic territorial polygons, basemap switcher,
 * centroid pulse markers, and floating Territory Inspector HUD.
 * — Sneha Kulkarni (Frontend UI/UX & GIS Map Specialist)
 * — Siddharth Rao (GIS Vector Tile & Rendering Optimizer)
 * — Rajesh Gupta (GIS & Remote Sensing Specialist)
 */

import { useEffect, useState, useMemo } from 'react';
import { MapContainer, TileLayer, GeoJSON, CircleMarker, Tooltip, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

export const PASTEL_RISK_COLORS = {
  very_high: '#FF8A8A', // pastel rose
  high: '#FFB3B3',      // pastel coral
  moderate: '#FFE0A3',  // pastel amber
  low: '#A8E6CF',       // pastel mint
  very_low: '#A3D5FF',  // pastel sky
};

const RISK_LABELS = {
  very_high: 'Very High Risk (>70%)',
  high: 'High Risk (50-70%)',
  moderate: 'Moderate Risk (30-50%)',
  low: 'Low Risk (10-30%)',
  very_low: 'Very Low Risk (<10%)',
};

const ONSET_LABELS = {
  active: 'High Onset Surge (>60%)',
  moderate: 'Moderate Onset (40-60%)',
  transition: 'Onset Transition (20-40%)',
  break: 'Monsoon Break / Low (<20%)',
};

const DRY_LABELS = {
  high_dry: 'High Dry Spell (>60%)',
  mod_dry: 'Moderate Dry Spell (40-60%)',
  low_dry: 'Mild Dry Spell (20-40%)',
  moist: 'Adequate Moisture (<20%)',
};

const BASEMAP_TILES = {
  topo: {
    name: '🏔️ Topo Terrain',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri, DeLorme, USGS, NPS',
    subdomains: 'abc',
  },
  canvas: {
    name: '🏙️ Pastel Canvas',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri, HERE, Garmin',
    subdomains: 'abc',
  },
  osm: {
    name: '🌐 OpenStreetMap',
    url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; OpenStreetMap contributors',
    subdomains: 'abc',
  },
  satellite: {
    name: '🛰️ Satellite Imagery',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: '&copy; Esri, Maxar, Earthstar Geographics',
    subdomains: 'abc',
  },
};

function MapController({ geojson, bounds, selectedBlockCode }) {
  const map = useMap();

  useEffect(() => {
    if (!map) return;

    // 1. If a specific block is selected, fly to it with smooth padding
    if (selectedBlockCode && geojson?.features) {
      const selectedFeature = geojson.features.find(
        (f) => f.properties?.location_code === selectedBlockCode
      );
      if (selectedFeature?.geometry?.coordinates?.[0]) {
        const coords = selectedFeature.geometry.coordinates[0].map(([lng, lat]) => [lat, lng]);
        map.fitBounds(coords, { padding: [60, 60], maxZoom: 11, animate: true, duration: 0.6 });
        return;
      }
    }

    // 2. Otherwise fit all features in geojson precisely
    if (geojson?.features && geojson.features.length > 0) {
      try {
        const allCoords = [];
        geojson.features.forEach((f) => {
          if (f.geometry?.coordinates?.[0]) {
            f.geometry.coordinates[0].forEach(([lng, lat]) => {
              allCoords.push([lat, lng]);
            });
          }
        });
        if (allCoords.length > 0) {
          map.fitBounds(allCoords, { padding: [45, 45], maxZoom: 10, animate: true, duration: 0.8 });
          return;
        }
      } catch (e) {
        console.warn('Error fitting geojson features bounds', e);
      }
    }

    // 3. Fallback to custom bounds or India default
    if (bounds && bounds.length === 2) {
      try {
        map.fitBounds(bounds, { padding: [40, 40], maxZoom: 10, animate: true, duration: 0.8 });
        return;
      } catch (e) {
        console.warn('Could not fit custom bounds', e);
      }
    }
  }, [geojson, bounds, selectedBlockCode, map]);

  return null;
}

export default function RiskMap({
  geojsonData,
  height = '530px',
  bounds = null,
  onBlockSelect = null,
  selectedBlockCode = null,
}) {
  const [key, setKey] = useState(0);
  const [activeLayer, setActiveLayer] = useState('risk'); // 'risk' | 'onset' | 'dry_spell'
  const [activeBasemap, setActiveBasemap] = useState('topo'); // 'topo' | 'canvas' | 'osm' | 'satellite'
  const [hoveredFeature, setHoveredFeature] = useState(null);

  useEffect(() => {
    if (geojsonData) {
      setKey((k) => k + 1);
    }
  }, [geojsonData, activeLayer, activeBasemap]);

  // Pick default inspection item if none hovered
  const displayedFeature = useMemo(() => {
    if (hoveredFeature) return hoveredFeature;
    if (geojsonData && geojsonData.features && geojsonData.features.length > 0) {
      if (selectedBlockCode) {
        const match = geojsonData.features.find((f) => f.properties?.location_code === selectedBlockCode);
        if (match) return match.properties;
      }
      return geojsonData.features[0].properties;
    }
    return null;
  }, [hoveredFeature, geojsonData, selectedBlockCode]);

  const getFeatureColor = (p) => {
    if (activeLayer === 'onset') {
      const prob = p.monsoon_onset_prob || 0;
      if (prob >= 60) return '#7BC9A0';
      if (prob >= 40) return '#A8E6CF';
      if (prob >= 20) return '#C9B8FF';
      return '#E2E4F0';
    }
    if (activeLayer === 'dry_spell') {
      const prob = p.dry_spell_prob || 0;
      if (prob >= 60) return '#FFE0A3';
      if (prob >= 40) return '#FFD4B8';
      if (prob >= 20) return '#A3D5FF';
      return '#A8E6CF';
    }
    // Default risk category
    return PASTEL_RISK_COLORS[p.risk_category] || '#A3D5FF';
  };

  const getStyle = (feature) => {
    const p = feature.properties || {};
    const isSelected = selectedBlockCode && p.location_code === selectedBlockCode;
    return {
      fillColor: getFeatureColor(p),
      weight: isSelected ? 3.5 : 2,
      opacity: 0.95,
      color: isSelected ? '#1A1D2E' : '#FFFFFF',
      fillOpacity: isSelected ? 0.88 : 0.72,
    };
  };

  const onEachFeature = (feature, layer) => {
    if (feature.properties) {
      const p = feature.properties;
      const riskColor = PASTEL_RISK_COLORS[p.risk_category] || '#0284C7';

      // Subtle permanent text label centered on block
      if (p.location_name) {
        layer.bindTooltip(p.location_name, {
          permanent: true,
          direction: 'center',
          className: 'block-map-label',
        });
      }

      layer.bindPopup(`
        <div style="font-family: Inter, sans-serif; min-width: 210px; padding: 2px;">
          <div class="popup-title">${p.location_name || 'Block'} ${p.district_name ? `(${p.district_name})` : ''}</div>
          <div class="popup-row">
            <span class="popup-label">State</span>
            <span class="popup-value" style="font-weight: 600;">${p.state_name || 'India'}</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">Risk Category</span>
            <span class="popup-value" style="color: ${riskColor}; font-weight: 700;">
              ${RISK_LABELS[p.risk_category] || p.risk_category}
            </span>
          </div>
          <div class="popup-row">
            <span class="popup-label">Rainfall Forecast</span>
            <span class="popup-value" style="font-weight: 700;">${p.rainfall_mm ?? '—'} mm</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">Heavy Rain Prob.</span>
            <span class="popup-value">${Math.round(p.heavy_rainfall_prob ?? 0)}%</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">Dry Spell Prob.</span>
            <span class="popup-value">${Math.round(p.dry_spell_prob ?? 0)}%</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">Onset Probability</span>
            <span class="popup-value">${Math.round(p.monsoon_onset_prob ?? 0)}%</span>
          </div>
          <div class="popup-row">
            <span class="popup-label">Confidence</span>
            <span class="popup-value">${Math.round((p.confidence || 0.85) * 100)}%</span>
          </div>
        </div>
      `);

      layer.on({
        mouseover: (e) => {
          setHoveredFeature(p);
          e.target.setStyle({
            fillOpacity: 0.94,
            weight: 3.5,
            color: '#1A1D2E',
          });
        },
        mouseout: (e) => {
          e.target.setStyle(getStyle(feature));
        },
        click: () => {
          if (onBlockSelect && p.location_code) {
            onBlockSelect(p.location_code);
          }
        },
      });
    }
  };

  const currentTile = BASEMAP_TILES[activeBasemap] || BASEMAP_TILES.topo;

  return (
    <div className="glass-card-static" style={{ overflow: 'hidden', position: 'relative' }}>
      {/* Header with Title and Resolution */}
      <div className="card-header" style={{ flexWrap: 'wrap', gap: '8px' }}>
        <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span>🗺️ Hyperlocal Spatial Risk Map</span>
          <span className="risk-badge low" style={{ fontSize: '0.72rem', padding: '3px 8px' }}>
            High-Res Topo Cartography
          </span>
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
          {/* Basemap Switcher */}
          <div className="basemap-switcher" style={{ display: 'flex', gap: '4px', background: 'rgba(255,255,255,0.7)', padding: '3px', borderRadius: '8px', border: '1px solid var(--border-soft)' }}>
            {Object.entries(BASEMAP_TILES).map(([keyName, bm]) => (
              <button
                key={keyName}
                onClick={() => setActiveBasemap(keyName)}
                style={{
                  fontSize: '0.72rem',
                  fontWeight: 600,
                  padding: '3px 8px',
                  borderRadius: '6px',
                  border: 'none',
                  cursor: 'pointer',
                  background: activeBasemap === keyName ? '#FFFFFF' : 'transparent',
                  color: activeBasemap === keyName ? '#1A1D2E' : 'var(--text-muted)',
                  boxShadow: activeBasemap === keyName ? '0 1px 4px rgba(0,0,0,0.1)' : 'none',
                  transition: 'all 0.15s ease',
                }}
              >
                {bm.name}
              </button>
            ))}
          </div>

          <span className="risk-badge very-low" style={{ fontSize: '0.72rem', padding: '3px 8px' }}>
            Organic Boundary Smoothing
          </span>
        </div>
      </div>

      {/* Layer Toggles Bar */}
      <div className="map-layer-toggles" style={{ padding: '8px 16px', background: '#F8F9FE', borderBottom: '1px solid var(--border-soft)' }}>
        <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-muted)' }}>
          Atmospheric Layers:
        </span>
        <button
          className={`layer-toggle-btn ${activeLayer === 'risk' ? 'active' : ''}`}
          onClick={() => setActiveLayer('risk')}
        >
          🌧️ Monsoon Rainfall Risk
        </button>
        <button
          className={`layer-toggle-btn onset ${activeLayer === 'onset' ? 'active' : ''}`}
          onClick={() => setActiveLayer('onset')}
        >
          🌊 Monsoon Onset Surge
        </button>
        <button
          className={`layer-toggle-btn dry ${activeLayer === 'dry_spell' ? 'active' : ''}`}
          onClick={() => setActiveLayer('dry_spell')}
        >
          ☀️ Dry Spell Vulnerability
        </button>
      </div>

      {/* Interactive Map Canvas */}
      <div style={{ height, position: 'relative' }}>
        <MapContainer
          center={[19.2, 75.2]}
          zoom={7}
          style={{ height: '100%', width: '100%' }}
          zoomControl={true}
        >
          <TileLayer
            key={activeBasemap}
            attribution={currentTile.attribution}
            url={currentTile.url}
            subdomains={currentTile.subdomains || 'abc'}
          />
          {geojsonData && geojsonData.features && (
            <>
              <GeoJSON
                key={`${key}-${activeBasemap}`}
                data={geojsonData}
                style={getStyle}
                onEachFeature={onEachFeature}
              />
              {/* Centroid Pulse Pins */}
              {geojsonData.features.map((f, i) => {
                const p = f.properties || {};
                const coords = p.centroid;
                if (!coords || coords.length < 2) return null;
                const riskColor = PASTEL_RISK_COLORS[p.risk_category] || '#0284C7';
                return (
                  <CircleMarker
                    key={`pin-${p.location_code || i}`}
                    center={coords}
                    radius={5}
                    pathOptions={{
                      fillColor: riskColor,
                      color: '#FFFFFF',
                      weight: 2,
                      fillOpacity: 1.0,
                    }}
                    eventHandlers={{
                      click: () => {
                        if (onBlockSelect && p.location_code) onBlockSelect(p.location_code);
                      },
                    }}
                  >
                    <Tooltip direction="top" offset={[0, -5]}>
                      <strong>{p.location_name}</strong>: {p.rainfall_mm ?? 0}mm ({p.risk_category?.replace('_', ' ')})
                    </Tooltip>
                  </CircleMarker>
                );
              })}
              <MapController geojson={geojsonData} bounds={bounds} selectedBlockCode={selectedBlockCode} />
            </>
          )}
        </MapContainer>

        {/* Floating Territory Inspector HUD Card */}
        {displayedFeature && (
          <div
            className="map-territory-hud"
            style={{
              position: 'absolute',
              top: 14,
              right: 14,
              zIndex: 1000,
              width: '240px',
              background: 'rgba(255, 255, 255, 0.94)',
              backdropFilter: 'blur(10px)',
              borderRadius: '12px',
              padding: '12px 14px',
              boxShadow: '0 8px 24px rgba(26, 29, 46, 0.12)',
              border: '1px solid rgba(226, 232, 240, 0.9)',
              pointerEvents: 'auto',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--text-dark)' }}>
                📍 {displayedFeature.location_name}
              </div>
              <span
                className={`risk-badge ${(displayedFeature.risk_category || 'low').replace('_', '-')}`}
                style={{ fontSize: '0.68rem', padding: '2px 7px' }}
              >
                {(displayedFeature.risk_category || 'low').replace('_', ' ')}
              </span>
            </div>

            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: 8 }}>
              {displayedFeature.district_name ? `${displayedFeature.district_name} District • ` : ''}
              {displayedFeature.state_name || 'Active Region'}
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px', marginBottom: 8, background: '#F8F9FE', padding: '6px 8px', borderRadius: '8px' }}>
              <div>
                <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>Rainfall (7d)</div>
                <div style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--text-dark)' }}>
                  {displayedFeature.rainfall_mm ?? '—'} mm
                </div>
              </div>
              <div>
                <div style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>Heavy Rain %</div>
                <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#D97706' }}>
                  {Math.round(displayedFeature.heavy_rainfall_prob ?? 0)}%
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--text-muted)', marginBottom: 6 }}>
              <span>Dry Spell Prob: <strong>{Math.round(displayedFeature.dry_spell_prob ?? 0)}%</strong></span>
              <span>Onset: <strong>{Math.round(displayedFeature.monsoon_onset_prob ?? 0)}%</strong></span>
            </div>

            <button
              className="btn btn-secondary btn-sm"
              style={{ width: '100%', fontSize: '0.74rem', padding: '4px 8px' }}
              onClick={() => {
                if (onBlockSelect && displayedFeature.location_code) {
                  onBlockSelect(displayedFeature.location_code);
                }
              }}
            >
              👉 Select {displayedFeature.location_name} for Advisories
            </button>
          </div>
        )}
      </div>

      {/* Dynamic Legend */}
      <div className="risk-legend" style={{ padding: '8px 16px', background: '#FFFFFF', borderTop: '1px solid var(--border-soft)' }}>
        {activeLayer === 'risk' && (
          Object.entries(RISK_LABELS).map(([k, label]) => (
            <div className="legend-item" key={k}>
              <div
                className="legend-dot"
                style={{ background: PASTEL_RISK_COLORS[k] }}
              />
              {label}
            </div>
          ))
        )}

        {activeLayer === 'onset' && (
          Object.entries(ONSET_LABELS).map(([k, label]) => {
            const colors = {
              active: '#7BC9A0',
              moderate: '#A8E6CF',
              transition: '#C9B8FF',
              break: '#E2E4F0',
            };
            return (
              <div className="legend-item" key={k}>
                <div className="legend-dot" style={{ background: colors[k] }} />
                {label}
              </div>
            );
          })
        )}

        {activeLayer === 'dry_spell' && (
          Object.entries(DRY_LABELS).map(([k, label]) => {
            const colors = {
              high_dry: '#FFE0A3',
              mod_dry: '#FFD4B8',
              low_dry: '#A3D5FF',
              moist: '#A8E6CF',
            };
            return (
              <div className="legend-item" key={k}>
                <div className="legend-dot" style={{ background: colors[k] }} />
                {label}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
