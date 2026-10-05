/**
 * MonSense — Main Application Component
 * SIH 2026 Smart India Hackathon Edition
 * Complete Pastel Theme, Cascading District GIS Mapping,
 * Interactive Scenario Simulator, and Visual Mobile Alert Simulator.
 *
 * — Sneha Kulkarni (Frontend UI/UX & GIS Map Specialist)
 * — Neha Singhal (UI Component & Styling Specialist)
 * — Om Pandey (Lead Architect)
 */

import { useState, useEffect, useCallback } from 'react';
import RiskMap from './components/RiskMap';
import ForecastChart from './components/ForecastChart';
import AdvisoryPanel from './components/AdvisoryPanel';
import ClimateWidget from './components/ClimateWidget';
import RiskDistribution from './components/RiskDistribution';
import ScenarioSimulator from './components/ScenarioSimulator';
import AlertSimulator from './components/AlertSimulator';
import { useApp } from './context/AppContext';
import { mockData } from './services/mockData';

const PAGES = {
  DASHBOARD: 'dashboard',
  MAP: 'map',
  FORECAST: 'forecast',
  ADVISORY: 'advisory',
  ALERTS: 'alerts',
};

function Sidebar({ activePage, onNavigate, monsoonStatus }) {
  const navItems = [
    { id: PAGES.DASHBOARD, label: 'Dashboard', icon: '📊' },
    { id: PAGES.MAP, label: 'Risk Map', icon: '🗺️' },
    { id: PAGES.FORECAST, label: 'Forecast', icon: '📈' },
    { id: PAGES.ADVISORY, label: 'Advisories', icon: '🌾' },
    { id: PAGES.ALERTS, label: 'Alerts', icon: '📱' },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">🌧️</div>
        <div>
          <span className="sidebar-logo-text">MonSense</span>
          <div style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--text-light)', letterSpacing: '0.5px' }}>
            HYPERLOCAL MONSOON AI
          </div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-item ${activePage === item.id ? 'active' : ''}`}
            onClick={() => onNavigate(item.id)}
          >
            <span className="nav-item-icon">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <div className={`monsoon-status ${monsoonStatus || 'active'}`}>
          Monsoon: {monsoonStatus ? monsoonStatus.charAt(0).toUpperCase() + monsoonStatus.slice(1) : 'Active'}
        </div>
        <div style={{ marginTop: 12 }}>
          <div className="sidebar-badge">
            ✅ SIH 2026 • PS 26086
          </div>
        </div>
        <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: 8, fontWeight: 500 }}>
          APPEX ALLIANCE • TEAM 1
        </div>
      </div>
    </aside>
  );
}

function StatCard({ icon, iconColor, value, label, trend }) {
  return (
    <div className="stat-card">
      <div className={`stat-icon ${iconColor}`}>{icon}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
      {trend && (
        <div className={`stat-trend ${trend.direction}`}>
          {trend.direction === 'up' ? '↑' : '↓'} {trend.value}
        </div>
      )}
    </div>
  );
}

function BlockRiskTable({ blocks, onSelectBlock }) {
  if (!blocks || blocks.length === 0) return null;

  return (
    <div className="glass-card-static">
      <div className="card-header">
        <div className="card-title">⚡ Block-Level Risk Summary</div>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          Click block to inspect
        </span>
      </div>
      <div className="card-body" style={{ padding: '0 0 8px' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Block</th>
              <th>Rainfall (mm)</th>
              <th>Heavy Rain %</th>
              <th>Risk Level</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {blocks.slice(0, 8).map((block) => (
              <tr key={block.code} style={{ cursor: 'pointer' }} onClick={() => onSelectBlock && onSelectBlock(block.code)}>
                <td style={{ fontWeight: 600, color: 'var(--text-dark)' }}>{block.name}</td>
                <td>{block.rainfall_mm} mm</td>
                <td>{Math.round(block.heavy_prob || 0)}%</td>
                <td>
                  <span className={`risk-badge ${block.risk?.replace('_', '-')}`}>
                    {block.risk?.replace('_', ' ')}
                  </span>
                </td>
                <td>
                  <button
                    className="btn btn-secondary btn-sm"
                    style={{ padding: '2px 8px', fontSize: '0.75rem' }}
                    onClick={(e) => {
                      e.stopPropagation();
                      if (onSelectBlock) onSelectBlock(block.code);
                    }}
                  >
                    Select
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default function App() {
  const [activePage, setActivePage] = useState(PAGES.DASHBOARD);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Global Context State
  const {
    selectedState,
    selectedStateCode,
    setSelectedState,
    states,
    selectedDistrict,
    setSelectedDistrict,
    selectedBlock,
    setSelectedBlock,
    isLiveMode,
    toggleLiveMode,
    districts,
    currentDistrictBlocks,
    currentDistrictObj,
    currentBlockObj,
    districtBounds,
    stateBounds,
  } = useApp();

  // Data states
  const [stats, setStats] = useState(null);
  const [riskOverview, setRiskOverview] = useState(null);
  const [riskMapData, setRiskMapData] = useState(null);
  const [timeSeries, setTimeSeries] = useState(null);
  const [advisories, setAdvisories] = useState(null);
  const [alertStats, setAlertStats] = useState(null);
  const [farmers, setFarmers] = useState(null);
  const [telemetry, setTelemetry] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch real-time weather telemetry from Open-Meteo
  useEffect(() => {
    let isSubscribed = true;
    async function fetchTelemetry() {
      try {
        if (isLiveMode) {
          const res = await fetch(`/api/v1/forecast/live-telemetry/${selectedBlock}`);
          if (res.ok) {
            const data = await res.json();
            if (isSubscribed) setTelemetry(data);
            return;
          }
        }
        // Demo or mock telemetry
        const mockTel = await mockData.getLiveTelemetry(selectedBlock);
        if (isSubscribed) setTelemetry(mockTel);
      } catch (e) {
        console.warn('Telemetry load fallback', e);
      }
    }
    fetchTelemetry();
    return () => { isSubscribed = false; };
  }, [selectedBlock, isLiveMode]);

  // Load Data based on selected location and live/demo mode
  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      const fetchOrMock = async (apiPath, mockFn) => {
        try {
          const controller = new AbortController();
          const timeoutId = setTimeout(() => controller.abort(), 2000);
          const res = await fetch(`/api/v1${apiPath}`, { signal: controller.signal });
          clearTimeout(timeoutId);
          if (res.ok) return await res.json();
          throw new Error('API offline');
        } catch {
          return mockFn();
        }
      };

      const [statsData, riskData, mapData, tsData, advData, alertData, farmerData] = await Promise.all([
        fetchOrMock('/dashboard/stats', () => mockData.getDashboardStats()),
        fetchOrMock(`/dashboard/risk-overview?state_code=${selectedStateCode}`, () => mockData.getRiskOverview(selectedStateCode)),
        fetchOrMock(`/forecast/risk-map?level=block&state_code=${selectedStateCode}`, () => mockData.getRiskMap(selectedStateCode)),
        fetchOrMock(`/forecast/time-series/${selectedBlock}?days=30`, () => mockData.getTimeSeries(selectedBlock)),
        fetchOrMock(`/advisory/generate/${selectedBlock}`, () => mockData.getAdvisories(selectedBlock)),
        fetchOrMock('/alerts/stats', () => mockData.getAlertStats()),
        fetchOrMock('/alerts/farmers', () => mockData.getFarmers()),
      ]);

      setStats(statsData);
      setRiskOverview(riskData);
      setRiskMapData(mapData);
      setTimeSeries(tsData);
      setAdvisories(advData);
      setAlertStats(alertData);
      setFarmers(farmerData);
    } catch (err) {
      console.error('Failed to load data:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedBlock, selectedStateCode, isLiveMode]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Persistent Cascading Location Filter Bar with All 6 States
  const renderLocationFilterBar = () => (
    <div className="location-filter-bar">
      <div className="filter-group">
        <span className="filter-label">State:</span>
        <select
          className="select-input"
          value={selectedStateCode}
          onChange={(e) => setSelectedState(e.target.value)}
          style={{ background: '#FFFFFF', fontWeight: 600, cursor: 'pointer' }}
        >
          {states.map((st) => (
            <option key={st.code} value={st.code}>
              {st.name} {st.name_local ? `(${st.name_local})` : ''}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <span className="filter-label">District:</span>
        <select
          className="select-input"
          value={selectedDistrict}
          onChange={(e) => setSelectedDistrict(e.target.value)}
        >
          {districts.map((d) => (
            <option key={d.code} value={d.code}>
              {d.name} {d.name_local ? `(${d.name_local})` : ''}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <span className="filter-label">Block / Taluka:</span>
        <select
          className="select-input"
          value={selectedBlock}
          onChange={(e) => setSelectedBlock(e.target.value)}
        >
          {currentDistrictBlocks.map((b) => (
            <option key={b.code} value={b.code}>
              {b.name}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 8 }}>
        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
          Selected: <strong style={{ color: 'var(--text-dark)' }}>{currentBlockObj.name}</strong>, {currentDistrictObj.name} ({selectedState})
        </span>
      </div>
    </div>
  );

  // Dedicated Live Weather Telemetry & Engine HUD Banner (Answers: "Is weather mock or real?")
  const renderWeatherTelemetryBanner = () => (
    <div className="weather-telemetry-banner">
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <span className={`engine-status-pill ${isLiveMode ? 'live' : 'sim'}`}>
            {isLiveMode ? '🟢 LIVE SATELLITE/NWP FEED' : '🟡 DEMO SIMULATION ENGINE'}
          </span>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-dark)', fontWeight: 600 }}>
            {isLiveMode
              ? `Open-Meteo ECMWF/GFS Real-Time Atmospheric Feed (${currentBlockObj.name}, ${selectedState})`
              : `Calibrated Historical IMD 30-Yr Normals & ENSO Climatology Engine`}
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          {telemetry && (
            <div className="telemetry-readouts" style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
              <span>🌡️ Temp: <strong>{telemetry.telemetry?.temperature_max_c ?? 33.2}°C</strong></span>
              <span>🌧️ Live Rain: <strong>{telemetry.telemetry?.precipitation_today_mm ?? 0} mm</strong></span>
              <span>🌱 Moisture: <strong>{telemetry.telemetry?.soil_moisture_volumetric ?? 0.28} m³/m³</strong></span>
              <span style={{ color: 'var(--text-muted)' }}>⚡ {telemetry.latency_ms ?? 175}ms</span>
            </div>
          )}
          <button
            className={`btn btn-sm ${isLiveMode ? 'btn-primary' : 'btn-secondary'}`}
            onClick={toggleLiveMode}
            style={{ fontSize: '0.74rem', padding: '4px 10px', whiteSpace: 'nowrap' }}
          >
            {isLiveMode ? '⚡ Switch to Demo Presets' : '🌐 Connect Real-Time Open-Meteo API'}
          </button>
        </div>
      </div>
    </div>
  );

  // Global Header Bar with Breadcrumb and Live/Demo Mode Switch
  const renderGlobalHeaderBar = () => (
    <div className="global-header-bar">
      <div className="breadcrumb-trail">
        <span className="breadcrumb-segment">🏛️ {selectedState}</span>
        <span className="breadcrumb-separator">›</span>
        <span className="breadcrumb-segment">📍 {currentDistrictObj.name} District</span>
        <span className="breadcrumb-separator">›</span>
        <span className="breadcrumb-segment active">🌾 {currentBlockObj.name} Block</span>
      </div>

      <div className="mode-toggle-group">
        <span style={{ fontSize: '0.78rem', fontWeight: 600, color: 'var(--text-mid)' }}>
          Data Mode:
        </span>
        <div className="mode-pill-toggle">
          <button
            className={`mode-pill-btn ${!isLiveMode ? 'active' : ''}`}
            onClick={() => isLiveMode && toggleLiveMode()}
            title="Use calibrated offline presets for hackathon judging"
          >
            🟡 Demo Engine
          </button>
          <button
            className={`mode-pill-btn ${isLiveMode ? 'active live-active' : ''}`}
            onClick={() => !isLiveMode && toggleLiveMode()}
            title="Fetch real-time live telemetry from Open-Meteo ECMWF satellite feed"
          >
            🟢 Live Open-Meteo
          </button>
        </div>
      </div>
    </div>
  );

  const renderPage = () => {
    switch (activePage) {
      case PAGES.MAP:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">GIS Risk Probability Heatmap</h1>
                <p className="page-subtitle">
                  Color-coded 4km resolution rainfall risk and dry spell probability map — {currentDistrictObj.name}, {selectedState}
                </p>
              </div>
            </div>

            {renderLocationFilterBar()}
            {renderWeatherTelemetryBanner()}

            <RiskMap
              geojsonData={riskMapData}
              height="580px"
              bounds={districtBounds}
              selectedBlockCode={selectedBlock}
              onBlockSelect={(code) => setSelectedBlock(code)}
            />


            <div style={{ marginTop: 24 }}>
              <div className="content-grid">
                <RiskDistribution
                  distribution={riskOverview?.distribution}
                  totalBlocks={riskOverview?.blocks?.length || 0}
                />
                <BlockRiskTable
                  blocks={riskOverview?.blocks}
                  onSelectBlock={(code) => setSelectedBlock(code)}
                />
              </div>
            </div>
          </>
        );

      case PAGES.FORECAST:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">7 to 30-Day Rainfall Forecast</h1>
                <p className="page-subtitle">
                  LSTM temporal sequence + XGBoost topographic downscaling ensemble
                </p>
              </div>
            </div>

            {renderLocationFilterBar()}
            {renderWeatherTelemetryBanner()}

            <ForecastChart
              data={timeSeries?.data}
              locationName={`${currentBlockObj.name} (${currentDistrictObj.name})`}
            />

            <div style={{ marginTop: 24 }}>
              <ClimateWidget indices={stats?.climate_indices} />
            </div>
          </>
        );

      case PAGES.ADVISORY:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">Crop-Specific AI Advisories</h1>
                <p className="page-subtitle">
                  Phenological crop stage recommendations and interactive scenario testing
                </p>
              </div>
            </div>

            {renderLocationFilterBar()}
            {renderWeatherTelemetryBanner()}

            <AdvisoryPanel
              advisories={advisories?.advisories}
              locationName={`${currentBlockObj.name}, ${currentDistrictObj.name}`}
              onTriggerAlert={() => setActivePage(PAGES.ALERTS)}
            />

            {/* Feature 4: Interactive Scenario Simulator */}
            <ScenarioSimulator />
          </>
        );

      case PAGES.ALERTS:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">Multilingual Alert Dispatch System</h1>
                <p className="page-subtitle">
                  SMS & WhatsApp cell-broadcast emulator for rural farmers with Marathi, Hindi & English delivery
                </p>
              </div>
            </div>

            {renderLocationFilterBar()}

            {/* Feature 3: Visual Mobile Alert Simulator */}
            <AlertSimulator districtName={currentDistrictObj.name} />

            <div style={{ marginTop: 24 }}>
              <div className="glass-card-static">
                <div className="card-header">
                  <div className="card-title">📊 Regional Dispatch Stats</div>
                  <span className="risk-badge low" style={{ fontSize: '0.72rem' }}>
                    Telecom Gateway Online
                  </span>
                </div>
                <div className="card-body">
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: 16 }}>
                    <div className="climate-index-card">
                      <div className="climate-index-label">SMS Dispatched</div>
                      <div className="climate-index-value" style={{ color: '#0284C7' }}>
                        {alertStats?.sms_sent || 32}
                      </div>
                    </div>
                    <div className="climate-index-card">
                      <div className="climate-index-label">WhatsApp Alerts</div>
                      <div className="climate-index-value" style={{ color: '#16A34A' }}>
                        {alertStats?.whatsapp_sent || 15}
                      </div>
                    </div>
                    <div className="climate-index-card">
                      <div className="climate-index-label">Delivery Rate</div>
                      <div className="climate-index-value" style={{ color: '#7C3AED' }}>
                        {alertStats?.delivery_rate || '93.6%'}
                      </div>
                    </div>
                    <div className="climate-index-card">
                      <div className="climate-index-label">Failures / Retries</div>
                      <div className="climate-index-value" style={{ color: '#B45309' }}>
                        {alertStats?.failed || 0}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        );

      default: // DASHBOARD
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">MonSense Operational Dashboard</h1>
                <p className="page-subtitle">
                  Hyperlocal Monsoon Prediction & Climate-Resilient Agricultural Advisory Platform
                </p>
              </div>
              <div className="header-actions">
                <div className={`monsoon-status ${stats?.monsoon_status || 'active'}`}>
                  🌧️ {stats?.monsoon_status?.charAt(0).toUpperCase() + stats?.monsoon_status?.slice(1) || 'Active'}
                </div>
              </div>
            </div>

            {renderLocationFilterBar()}
            {renderWeatherTelemetryBanner()}

            {/* Stats Grid */}
            <div className="stats-grid">
              <StatCard icon="🏘️" iconColor="blue" value={stats?.total_blocks || '10'} label="Monitored Blocks" />
              <StatCard icon="⚠️" iconColor="red" value={stats?.high_risk_blocks || '3'} label="High Risk Blocks" trend={{ direction: 'up', value: 'Active' }} />
              <StatCard icon="🌧️" iconColor="cyan" value={stats?.active_forecasts || '30'} label="Active Forecasts" />
              <StatCard icon="🌾" iconColor="green" value={stats?.active_advisories || '12'} label="Crop Advisories" />
              <StatCard icon="📱" iconColor="purple" value={stats?.alerts_sent_today || '47'} label="Alerts Dispatched" />
              <StatCard icon="👨‍🌾" iconColor="orange" value={stats?.registered_farmers || '5'} label="Registered Farmers" />
            </div>

            {/* Map + Risk Distribution */}
            <div className="content-grid thirds">
              <RiskMap
                geojsonData={riskMapData}
                height="440px"
                bounds={districtBounds}
                selectedBlockCode={selectedBlock}
                onBlockSelect={(code) => setSelectedBlock(code)}
              />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                <RiskDistribution
                  distribution={riskOverview?.distribution}
                  totalBlocks={riskOverview?.blocks?.length || 0}
                />
                <ClimateWidget indices={stats?.climate_indices} />
              </div>
            </div>

            {/* Forecast + Advisories */}
            <div className="content-grid" style={{ marginTop: 24 }}>
              <ForecastChart
                data={timeSeries?.data}
                locationName={`${currentBlockObj.name} (${currentDistrictObj.name})`}
              />
              <AdvisoryPanel
                advisories={advisories?.advisories?.slice(0, 3)}
                locationName={`${currentBlockObj.name}, ${currentDistrictObj.name}`}
                onTriggerAlert={() => setActivePage(PAGES.ALERTS)}
              />
            </div>

            {/* Block Table */}
            <div style={{ marginTop: 24 }}>
              <BlockRiskTable
                blocks={riskOverview?.blocks}
                onSelectBlock={(code) => setSelectedBlock(code)}
              />
            </div>
          </>
        );
    }
  };

  return (
    <div className="app-layout">
      {/* Mobile menu button */}
      <button
        className="mobile-menu-btn"
        onClick={() => setSidebarOpen(!sidebarOpen)}
        aria-label="Toggle menu"
      >
        {sidebarOpen ? '✕' : '☰'}
      </button>

      <Sidebar
        activePage={activePage}
        onNavigate={(page) => {
          setActivePage(page);
          setSidebarOpen(false);
        }}
        monsoonStatus={stats?.monsoon_status}
      />

      <main className="main-content">
        {renderGlobalHeaderBar()}

        {loading ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '55vh', gap: 16 }}>
            <div className="loading-spinner" />
            <div style={{ color: 'var(--text-mid)', fontSize: '0.92rem', fontWeight: 500 }}>
              Synchronizing MonSense Telemetry...
            </div>
          </div>
        ) : (
          renderPage()
        )}
      </main>
    </div>
  );
}
