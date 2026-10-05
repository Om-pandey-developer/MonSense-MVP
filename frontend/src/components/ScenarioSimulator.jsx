/**
 * MonSense Scenario Simulator Component
 * Interactive what-if simulator testing rainfall bursts and dry spell agronomic scenarios.
 * — Dr. Meenakshi Iyer & Sneha Kulkarni
 */

import { useState, useMemo } from 'react';
import { mockData } from '../services/mockData';

const CROPS = [
  { id: 'rice', label: 'Rice (धान)' },
  { id: 'soybean', label: 'Soybean (सोयाबीन)' },
  { id: 'cotton', label: 'Cotton (कपास)' },
  { id: 'wheat', label: 'Wheat (गेहूँ)' },
  { id: 'sugarcane', label: 'Sugarcane (गन्ना)' },
  { id: 'maize', label: 'Maize (मक्का)' },
  { id: 'groundnut', label: 'Groundnut (मूंगफली)' },
  { id: 'pulses', label: 'Pulses (दालें)' },
];

const STAGES = [
  { id: 'pre_sowing', label: 'Pre-Sowing (बुवाई पूर्व)' },
  { id: 'sowing', label: 'Sowing (बुवाई)' },
  { id: 'vegetative', label: 'Vegetative (वानस्पतिक)' },
  { id: 'flowering', label: 'Flowering (फूल आना)' },
  { id: 'maturity', label: 'Maturity (परिपक्वता)' },
  { id: 'harvest', label: 'Harvest (कटाई)' },
];

export default function ScenarioSimulator() {
  const [rainfallMm, setRainfallMm] = useState(65);
  const [drySpellDays, setDrySpellDays] = useState(2);
  const [selectedCrop, setSelectedCrop] = useState('rice');
  const [selectedStage, setSelectedStage] = useState('flowering');

  // Compute live simulated advisories
  const simulationResult = useMemo(() => {
    return mockData.simulateAdvisory({
      rainfall_mm: rainfallMm,
      dry_spell_days: drySpellDays,
      crop: selectedCrop,
      crop_stage: selectedStage,
    });
  }, [rainfallMm, drySpellDays, selectedCrop, selectedStage]);

  // Preset Handlers
  const applyPreset = (rain, dry, crop, stage) => {
    setRainfallMm(rain);
    setDrySpellDays(dry);
    if (crop) setSelectedCrop(crop);
    if (stage) setSelectedStage(stage);
  };

  return (
    <div className="glass-card-static" style={{ marginTop: 24 }}>
      <div className="card-header">
        <div className="card-title">
          🧪 Interactive Crop Scenario Simulator
        </div>
        <span className="risk-badge low" style={{ fontSize: '0.72rem' }}>
          Real-Time Rule Engine Evaluation
        </span>
      </div>

      <div className="card-body">
        {/* Preset scenario shortcuts */}
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: 8 }}>
            DEMO PRESET SCENARIOS:
          </div>
          <div className="preset-pills">
            <button
              className="preset-pill-btn"
              onClick={() => applyPreset(85, 0, 'rice', 'flowering')}
            >
              ⛈️ Heavy Rainfall (85mm)
            </button>
            <button
              className="preset-pill-btn"
              onClick={() => applyPreset(4, 14, 'soybean', 'flowering')}
            >
              ☀️ Severe Dry Spell (14 Days)
            </button>
            <button
              className="preset-pill-btn"
              onClick={() => applyPreset(45, 2, 'cotton', 'sowing')}
            >
              🌱 Optimal Sowing Window (45mm)
            </button>
            <button
              className="preset-pill-btn"
              onClick={() => applyPreset(120, 0, 'sugarcane', 'vegetative')}
            >
              🌊 Flash Flood Surge (120mm)
            </button>
          </div>
        </div>

        {/* Controls Layout */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 20, marginBottom: 24 }}>
          {/* Rainfall Slider */}
          <div className="slider-group">
            <div className="slider-header">
              <span>Forecast Rainfall (mm)</span>
              <span className="slider-value-badge" style={{ background: '#E0F2FE', color: '#0369A1' }}>
                {rainfallMm} mm
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="150"
              step="5"
              value={rainfallMm}
              onChange={(e) => setRainfallMm(Number(e.target.value))}
              className="range-slider"
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-light)' }}>
              <span>0mm (Dry)</span>
              <span>65mm (Heavy)</span>
              <span>150mm (Extreme)</span>
            </div>
          </div>

          {/* Dry Spell Slider */}
          <div className="slider-group">
            <div className="slider-header">
              <span>Dry Spell Duration</span>
              <span className="slider-value-badge" style={{ background: '#FEF3C7', color: '#B45309' }}>
                {drySpellDays} Days
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="25"
              step="1"
              value={drySpellDays}
              onChange={(e) => setDrySpellDays(Number(e.target.value))}
              className="range-slider"
            />
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', color: 'var(--text-light)' }}>
              <span>0 days</span>
              <span>7 days (Warning)</span>
              <span>25 days (Critical)</span>
            </div>
          </div>

          {/* Crop Dropdown */}
          <div>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-dark)', marginBottom: 6 }}>
              Target Crop
            </div>
            <select
              className="select-input"
              style={{ width: '100%' }}
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
            >
              {CROPS.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.label}
                </option>
              ))}
            </select>
          </div>

          {/* Growth Stage Dropdown */}
          <div>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-dark)', marginBottom: 6 }}>
              Phenological Stage
            </div>
            <select
              className="select-input"
              style={{ width: '100%' }}
              value={selectedStage}
              onChange={(e) => setSelectedStage(e.target.value)}
            >
              {STAGES.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Live Evaluated Advisories */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
            <span style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--text-dark)' }}>
              💡 Real-Time Generated Agronomic Advisories
            </span>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
              {simulationResult.advisories.length} recommendations triggered
            </span>
          </div>

          <div className="advisory-list">
            {simulationResult.advisories.map((adv, idx) => (
              <div key={idx} className={`advisory-card ${adv.severity}`}>
                <div className="advisory-header">
                  <span className="advisory-crop">
                    {adv.crop_name} — <span style={{ color: 'var(--text-muted)', fontWeight: 500, fontSize: '0.82rem' }}>
                      {adv.crop_stage?.replace('_', ' ')}
                    </span>
                  </span>
                  <span className={`risk-badge ${adv.severity === 'critical' ? 'very-high' : adv.severity === 'warning' ? 'high' : 'low'}`}>
                    {adv.severity}
                  </span>
                </div>
                <div className="advisory-text" style={{ fontWeight: 500, color: '#1A1D2E' }}>
                  {adv.advisory_text_en}
                </div>
                {adv.advisory_text_hi && (
                  <div className="advisory-text" style={{ marginTop: 6, fontStyle: 'normal', color: '#4A4E69', background: '#F8F9FE', padding: '6px 10px', borderRadius: '6px', borderLeft: '3px solid #C9B8FF' }}>
                    🇮🇳 {adv.advisory_text_hi}
                  </div>
                )}
                {adv.actions && (
                  <div className="advisory-actions">
                    {Object.entries(adv.actions).map(([key, value]) => (
                      <span key={key} className="action-tag">
                        ✓ {value}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
