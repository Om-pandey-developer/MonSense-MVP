/**
 * MonSense Advisory Panel Component
 * Displays crop-specific advisories with pastel severity indicators and bilingual guidance.
 * — Dr. Meenakshi Iyer (Agricultural Scientist)
 */

export default function AdvisoryPanel({ advisories, locationName, onTriggerAlert }) {
  if (!advisories || advisories.length === 0) {
    return (
      <div className="glass-card-static">
        <div className="card-header">
          <div className="card-title">🌾 Crop Advisories</div>
        </div>
        <div className="card-body" style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px 24px' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>🌱</div>
          <div style={{ fontWeight: 600, color: 'var(--text-dark)' }}>No active crop advisories for this location</div>
          <div style={{ fontSize: '0.85rem', marginTop: 4 }}>Conditions are within normal agronomic thresholds</div>
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card-static">
      <div className="card-header">
        <div className="card-title">
          🌾 Crop Advisories — {locationName || 'Selected Block'}
        </div>
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <span style={{
            fontSize: '0.8rem',
            color: '#15803D',
            fontWeight: 600,
            background: '#DCFCE7',
            padding: '3px 10px',
            borderRadius: '9999px',
          }}>
            {advisories.length} Active Rules
          </span>
          {onTriggerAlert && (
            <button
              className="btn btn-coral btn-sm"
              style={{ padding: '3px 10px', fontSize: '0.75rem' }}
              onClick={onTriggerAlert}
              title="Broadcast emergency advisory alert to farmers"
            >
              📢 Send Advisory Alert
            </button>
          )}
        </div>
      </div>
      <div className="card-body">
        <div className="advisory-list">
          {advisories.map((adv, idx) => (
            <div key={idx} className={`advisory-card ${adv.severity}`}>
              <div className="advisory-header">
                <span className="advisory-crop">
                  {adv.crop_name ? adv.crop_name.toUpperCase() : 'CROP'} — <span style={{ color: 'var(--text-muted)', fontWeight: 500, fontSize: '0.82rem' }}>
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
  );
}
