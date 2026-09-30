/**
 * MonSense Advisory Panel Component
 * Displays crop-specific advisories with severity indicators.
 * — Dr. Meenakshi Iyer (Agricultural Scientist)
 */

export default function AdvisoryPanel({ advisories, locationName }) {
  if (!advisories || advisories.length === 0) {
    return (
      <div className="glass-card-static">
        <div className="card-header">
          <div className="card-title">🌾 Crop Advisories</div>
        </div>
        <div className="card-body" style={{ color: 'var(--text-muted)', textAlign: 'center', padding: '40px 24px' }}>
          <div style={{ fontSize: '2rem', marginBottom: 8 }}>🌱</div>
          <div>No active advisories for this location</div>
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
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          {advisories.length} active
        </span>
      </div>
      <div className="card-body">
        <div className="advisory-list">
          {advisories.map((adv, idx) => (
            <div key={idx} className={`advisory-card ${adv.severity}`}>
              <div className="advisory-header">
                <span className="advisory-crop">
                  {adv.crop_name} — <span style={{ color: 'var(--text-muted)', fontWeight: 400, fontSize: '0.8rem' }}>{adv.crop_stage}</span>
                </span>
                <span className={`risk-badge ${adv.severity === 'critical' ? 'very-high' : adv.severity === 'warning' ? 'high' : 'low'}`}>
                  {adv.severity}
                </span>
              </div>
              <div className="advisory-text">
                {adv.advisory_text_en}
              </div>
              {adv.advisory_text_hi && (
                <div className="advisory-text" style={{ marginTop: 6, fontStyle: 'italic', opacity: 0.8 }}>
                  {adv.advisory_text_hi}
                </div>
              )}
              {adv.actions && (
                <div className="advisory-actions">
                  {Object.entries(adv.actions).map(([key, value]) => (
                    <span key={key} className="action-tag">
                      {value}
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
