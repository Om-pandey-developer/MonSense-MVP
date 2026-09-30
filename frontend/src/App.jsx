/**
 * MonSense — Main Application Component
 * Premium glassmorphism dashboard with sidebar navigation.
 *
 * — Sneha Kulkarni (Frontend UI/UX & GIS Map Specialist)
 * — Neha Singhal (UI Component & CSS Specialist)
 * — Om Pandey (Lead Architect)
 */

import { useState, useEffect, useCallback } from 'react';
import RiskMap from './components/RiskMap';
import ForecastChart from './components/ForecastChart';
import AdvisoryPanel from './components/AdvisoryPanel';
import ClimateWidget from './components/ClimateWidget';
import RiskDistribution from './components/RiskDistribution';
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
        <span className="sidebar-logo-text">MonSense</span>
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
        <div className={`monsoon-status ${monsoonStatus || 'off-season'}`}>
          Monsoon: {monsoonStatus ? monsoonStatus.charAt(0).toUpperCase() + monsoonStatus.slice(1) : 'Off-Season'}
        </div>
        <div style={{ marginTop: 12 }}>
          <div className="sidebar-badge">
            ✅ SIH 2026 • PS 26086
          </div>
        </div>
        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: 8 }}>
          APPEX ALLIANCE
        </div>
      </div>
    </aside>
  );
}

function StatCard({ icon, iconColor, value, label, trend }) {
  return (
    <div className="glass-card stat-card">
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

function BlockRiskTable({ blocks }) {
  if (!blocks || blocks.length === 0) return null;

  return (
    <div className="glass-card-static">
      <div className="card-header">
        <div className="card-title">⚡ Block-Level Risk Summary</div>
      </div>
      <div className="card-body" style={{ padding: '0 0 8px' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Block</th>
              <th>Rainfall (mm)</th>
              <th>Heavy Rain %</th>
              <th>Risk Level</th>
            </tr>
          </thead>
          <tbody>
            {blocks.slice(0, 8).map((block) => (
              <tr key={block.code}>
                <td style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{block.name}</td>
                <td>{block.rainfall_mm} mm</td>
                <td>{Math.round(block.heavy_prob)}%</td>
                <td>
                  <span className={`risk-badge ${block.risk?.replace('_', '-')}`}>
                    {block.risk?.replace('_', ' ')}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function AlertsPanel({ stats, farmers }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      <div className="glass-card-static">
        <div className="card-header">
          <div className="card-title">📊 Alert Statistics</div>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16 }}>
            <div className="climate-index-card">
              <div className="climate-index-label">SMS Sent</div>
              <div className="climate-index-value" style={{ color: '#38bdf8' }}>{stats?.sms_sent || 0}</div>
            </div>
            <div className="climate-index-card">
              <div className="climate-index-label">WhatsApp</div>
              <div className="climate-index-value" style={{ color: '#22c55e' }}>{stats?.whatsapp_sent || 0}</div>
            </div>
            <div className="climate-index-card">
              <div className="climate-index-label">Delivery Rate</div>
              <div className="climate-index-value" style={{ color: '#c084fc' }}>{stats?.delivery_rate || 'N/A'}</div>
            </div>
          </div>
        </div>
      </div>

      <div className="glass-card-static">
        <div className="card-header">
          <div className="card-title">👨‍🌾 Registered Farmers</div>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            {farmers?.length || 0} farmers
          </span>
        </div>
        <div className="card-body" style={{ padding: '0 0 8px' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Phone</th>
                <th>Crops</th>
                <th>Language</th>
              </tr>
            </thead>
            <tbody>
              {(farmers || []).map((f) => (
                <tr key={f.id}>
                  <td style={{ fontWeight: 500, color: 'var(--text-primary)' }}>{f.name}</td>
                  <td>{f.phone}</td>
                  <td>
                    <div style={{ display: 'flex', gap: 4, flexWrap: 'wrap' }}>
                      {(f.crops || []).map((c) => (
                        <span key={c} className="action-tag">{c}</span>
                      ))}
                    </div>
                  </td>
                  <td>{f.language_preference?.toUpperCase()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [activePage, setActivePage] = useState(PAGES.DASHBOARD);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Data states
  const [stats, setStats] = useState(null);
  const [riskOverview, setRiskOverview] = useState(null);
  const [riskMapData, setRiskMapData] = useState(null);
  const [timeSeries, setTimeSeries] = useState(null);
  const [advisories, setAdvisories] = useState(null);
  const [alertStats, setAlertStats] = useState(null);
  const [farmers, setFarmers] = useState(null);
  const [selectedBlock, setSelectedBlock] = useState('MH-PUN-BAR');
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    setLoading(true);
    try {
      // Try API first, fall back to mock
      const fetchOrMock = async (apiPath, mockFn) => {
        try {
          const res = await fetch(`/api/v1${apiPath}`);
          if (res.ok) return await res.json();
          throw new Error('API unavailable');
        } catch {
          return mockFn();
        }
      };

      const [statsData, riskData, mapData, tsData, advData, alertData, farmerData] = await Promise.all([
        fetchOrMock('/dashboard/stats', () => mockData.getDashboardStats()),
        fetchOrMock('/dashboard/risk-overview', () => mockData.getRiskOverview()),
        fetchOrMock('/forecast/risk-map?level=block', () => mockData.getRiskMap()),
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
  }, [selectedBlock]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const renderPage = () => {
    switch (activePage) {
      case PAGES.MAP:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">Risk Probability Map</h1>
                <p className="page-subtitle">Block/village-level color-coded risk heatmap — Maharashtra</p>
              </div>
            </div>
            <RiskMap geojsonData={riskMapData} height="600px" />
            <div style={{ marginTop: 20 }}>
              <div className="content-grid">
                <RiskDistribution
                  distribution={riskOverview?.distribution}
                  totalBlocks={riskOverview?.blocks?.length || 0}
                />
                <BlockRiskTable blocks={riskOverview?.blocks} />
              </div>
            </div>
          </>
        );

      case PAGES.FORECAST:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">7-30 Day Forecast</h1>
                <p className="page-subtitle">Time-series rainfall prediction with LSTM + XGBoost ensemble</p>
              </div>
              <div className="header-actions">
                <select
                  className="select-input"
                  value={selectedBlock}
                  onChange={(e) => setSelectedBlock(e.target.value)}
                >
                  <option value="MH-PUN-BAR">Baramati</option>
                  <option value="MH-PUN-IND">Indapur</option>
                  <option value="MH-PUN-JUN">Junnar</option>
                  <option value="MH-PUN-HAV">Haveli</option>
                  <option value="MH-PUN-MUL">Mulshi</option>
                  <option value="MH-PUN-SHR">Shirur</option>
                  <option value="MH-NAG-RUR">Nagpur Rural</option>
                  <option value="MH-NAG-KAM">Kamptee</option>
                  <option value="MH-NAS-IGT">Igatpuri</option>
                  <option value="MH-NAS-MAL">Malegaon</option>
                </select>
              </div>
            </div>
            <ForecastChart
              data={timeSeries?.data}
              locationName={selectedBlock.split('-').pop()}
            />
            <div style={{ marginTop: 20 }}>
              <ClimateWidget indices={stats?.climate_indices} />
            </div>
          </>
        );

      case PAGES.ADVISORY:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">Crop-Specific Advisories</h1>
                <p className="page-subtitle">AI-generated farming recommendations based on forecast data</p>
              </div>
              <div className="header-actions">
                <select
                  className="select-input"
                  value={selectedBlock}
                  onChange={(e) => setSelectedBlock(e.target.value)}
                >
                  <option value="MH-PUN-BAR">Baramati</option>
                  <option value="MH-PUN-IND">Indapur</option>
                  <option value="MH-PUN-JUN">Junnar</option>
                  <option value="MH-NAG-RUR">Nagpur Rural</option>
                  <option value="MH-NAS-IGT">Igatpuri</option>
                </select>
              </div>
            </div>
            <AdvisoryPanel
              advisories={advisories?.advisories}
              locationName={advisories?.location?.name || selectedBlock.split('-').pop()}
            />
          </>
        );

      case PAGES.ALERTS:
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">Alert Management</h1>
                <p className="page-subtitle">SMS & WhatsApp alert broadcast system — Regional language delivery</p>
              </div>
            </div>
            <AlertsPanel stats={alertStats} farmers={farmers?.farmers} />
          </>
        );

      default: // DASHBOARD
        return (
          <>
            <div className="page-header">
              <div>
                <h1 className="page-title">MonSense Dashboard</h1>
                <p className="page-subtitle">
                  Hyperlocal Monsoon Prediction & Crop Advisory Platform — Maharashtra
                </p>
              </div>
              <div className="header-actions">
                <div className={`monsoon-status ${stats?.monsoon_status || 'off-season'}`}>
                  🌧️ {stats?.monsoon_status?.charAt(0).toUpperCase() + stats?.monsoon_status?.slice(1) || 'Loading...'}
                </div>
              </div>
            </div>

            {/* Stats Grid */}
            <div className="stats-grid">
              <StatCard icon="🏘️" iconColor="blue" value={stats?.total_blocks || '—'} label="Monitored Blocks" />
              <StatCard icon="⚠️" iconColor="red" value={stats?.high_risk_blocks || '—'} label="High Risk Blocks" trend={{ direction: 'up', value: 'Active' }} />
              <StatCard icon="🌧️" iconColor="cyan" value={stats?.active_forecasts || '—'} label="Active Forecasts" />
              <StatCard icon="🌾" iconColor="green" value={stats?.active_advisories || '—'} label="Crop Advisories" />
              <StatCard icon="📱" iconColor="purple" value={stats?.alerts_sent_today || '—'} label="Alerts Today" />
              <StatCard icon="👨‍🌾" iconColor="orange" value={stats?.registered_farmers || '—'} label="Farmers Registered" />
            </div>

            {/* Map + Risk Distribution */}
            <div className="content-grid thirds">
              <RiskMap geojsonData={riskMapData} height="420px" />
              <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
                <RiskDistribution
                  distribution={riskOverview?.distribution}
                  totalBlocks={riskOverview?.blocks?.length || 0}
                />
                <ClimateWidget indices={stats?.climate_indices} />
              </div>
            </div>

            {/* Forecast + Advisories */}
            <div className="content-grid" style={{ marginTop: 20 }}>
              <ForecastChart
                data={timeSeries?.data}
                locationName={selectedBlock.split('-').pop()}
              />
              <AdvisoryPanel
                advisories={advisories?.advisories?.slice(0, 3)}
                locationName="Baramati"
              />
            </div>

            {/* Block Table */}
            <div style={{ marginTop: 20 }}>
              <BlockRiskTable blocks={riskOverview?.blocks} />
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
        {loading ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: 16 }}>
            <div className="loading-spinner" />
            <div style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Loading MonSense data...</div>
          </div>
        ) : (
          renderPage()
        )}
      </main>
    </div>
  );
}
