/**
 * MonSense Risk Map Component
 * Interactive Leaflet.js heatmap with color-coded risk polygons.
 * — Sneha Kulkarni (Frontend UI/UX & GIS Map Specialist)
 * — Siddharth Rao (GIS Vector Tile & Rendering Optimizer)
 * — Rajesh Gupta (GIS & Remote Sensing Specialist)
 */

import { useEffect, useRef, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const RISK_COLORS = {
  very_high: '#ef4444',
  high: '#f97316',
  moderate: '#eab308',
  low: '#22c55e',
  very_low: '#06b6d4',
};

const RISK_LABELS = {
  very_high: 'Very High (70-100%)',
  high: 'High (50-70%)',
  moderate: 'Moderate (30-50%)',
  low: 'Low (10-30%)',
  very_low: 'Very Low (0-10%)',
};

function FitBounds({ geojson }) {
  const map = useMap();
  useEffect(() => {
    if (geojson && geojson.features && geojson.features.length > 0) {
      try {
        const bounds = [];
        geojson.features.forEach((f) => {
          if (f.geometry && f.geometry.coordinates) {
            f.geometry.coordinates[0].forEach(([lng, lat]) => {
              bounds.push([lat, lng]);
            });
          }
        });
        if (bounds.length > 0) {
          map.fitBounds(bounds, { padding: [30, 30] });
        }
      } catch (e) {
        // fallback center
        map.setView([19.0, 75.0], 7);
      }
    }
  }, [geojson, map]);
  return null;
}

function getStyle(feature) {
  const risk = feature.properties.risk_category;
  return {
    fillColor: RISK_COLORS[risk] || '#64748b',
    weight: 1.5,
    opacity: 0.8,
    color: '#ffffff30',
    fillOpacity: 0.55,
  };
}

function onEachFeature(feature, layer) {
  if (feature.properties) {
    const p = feature.properties;
    const riskColor = RISK_COLORS[p.risk_category] || '#999';

    layer.bindPopup(`
      <div>
        <div class="popup-title">${p.location_name}</div>
        <div class="popup-row">
          <span class="popup-label">Risk Level</span>
          <span class="popup-value" style="color: ${riskColor}">${RISK_LABELS[p.risk_category] || p.risk_category}</span>
        </div>
        <div class="popup-row">
          <span class="popup-label">Predicted Rainfall</span>
          <span class="popup-value">${p.rainfall_mm} mm</span>
        </div>
        <div class="popup-row">
          <span class="popup-label">Heavy Rain Prob.</span>
          <span class="popup-value">${Math.round(p.heavy_rainfall_prob)}%</span>
        </div>
        <div class="popup-row">
          <span class="popup-label">Dry Spell Prob.</span>
          <span class="popup-value">${Math.round(p.dry_spell_prob)}%</span>
        </div>
        <div class="popup-row">
          <span class="popup-label">Flood Risk</span>
          <span class="popup-value">${Math.round(p.flood_risk_prob)}%</span>
        </div>
        <div class="popup-row">
          <span class="popup-label">Confidence</span>
          <span class="popup-value">${Math.round((p.confidence || 0) * 100)}%</span>
        </div>
      </div>
    `);

    layer.on({
      mouseover: (e) => {
        e.target.setStyle({
          fillOpacity: 0.8,
          weight: 2.5,
          color: '#ffffff60',
        });
      },
      mouseout: (e) => {
        e.target.setStyle(getStyle(feature));
      },
    });
  }
}

export default function RiskMap({ geojsonData, height = '500px' }) {
  const [key, setKey] = useState(0);

  useEffect(() => {
    if (geojsonData) {
      setKey((k) => k + 1);
    }
  }, [geojsonData]);

  return (
    <div className="glass-card-static" style={{ overflow: 'hidden' }}>
      <div className="card-header">
        <div className="card-title">
          🗺️ Block/Village Risk Probability Map
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <span className="risk-badge moderate" style={{ fontSize: '0.7rem' }}>
            Interactive — Click a region for details
          </span>
        </div>
      </div>

      <div style={{ height, position: 'relative' }}>
        <MapContainer
          center={[19.0, 75.0]}
          zoom={7}
          style={{ height: '100%', width: '100%' }}
          zoomControl={true}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {geojsonData && geojsonData.features && (
            <>
              <GeoJSON
                key={key}
                data={geojsonData}
                style={getStyle}
                onEachFeature={onEachFeature}
              />
              <FitBounds geojson={geojsonData} />
            </>
          )}
        </MapContainer>
      </div>

      <div className="risk-legend">
        {Object.entries(RISK_LABELS).map(([key, label]) => (
          <div className="legend-item" key={key}>
            <div
              className="legend-dot"
              style={{ background: RISK_COLORS[key] }}
            />
            {label}
          </div>
        ))}
      </div>
    </div>
  );
}
