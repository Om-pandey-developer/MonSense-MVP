/**
 * MonSense Climate Indices Widget
 * Displays ENSO, IOD, and MJO teleconnection indices with visual pastel gauges.
 * — Dr. Aarav Sharma (Chief Climatologist)
 */

export default function ClimateWidget({ indices }) {
  if (!indices) return null;

  const { enso, iod, mjo } = indices;

  const getPhaseClass = (phase) => {
    if (!phase) return 'phase-neutral';
    const p = phase.toLowerCase();
    if (p.includes('positive') || p.includes('niña') || p.includes('la')) return 'phase-positive';
    if (p.includes('negative') || p.includes('niño') || p.includes('el')) return 'phase-negative';
    return 'phase-neutral';
  };

  // ENSO position: -2.5 to +2.5 mapped to 0% - 100%
  const ninoVal = enso?.nino34 ?? 0;
  const ensoPercent = Math.min(100, Math.max(0, ((ninoVal + 2.5) / 5.0) * 100));

  // IOD position: -1.0 to +1.0 mapped to 0% - 100%
  const iodVal = iod?.dmi ?? 0;
  const iodPercent = Math.min(100, Math.max(0, ((iodVal + 1.0) / 2.0) * 100));

  // ENSO impact text
  const ensoImpact = ninoVal > 0.5
    ? 'El Niño active: elevated risk of deficit monsoon & dry spells'
    : ninoVal < -0.5
    ? 'La Niña active: favorable for above-normal monsoon rainfall'
    : 'Neutral ENSO: normal climatic baseline conditions';

  // IOD impact text
  const iodImpact = iodVal > 0.4
    ? 'Positive IOD: enhances moisture surge over Western Ghats'
    : iodVal < -0.4
    ? 'Negative IOD: dampens South Asian monsoon intensity'
    : 'Neutral IOD: minimal anomalous dipole influence';

  // MJO impact text
  const mjoPhase = mjo?.phase ?? 3;
  const mjoImpact = (mjoPhase >= 2 && mjoPhase <= 4)
    ? 'MJO in Indian Ocean: actively enhances convective rain bursts'
    : 'MJO in Pacific: suppressed convective phase over India';

  return (
    <div className="glass-card-static">
      <div className="card-header">
        <div className="card-title">🌍 Climate Teleconnection Indices</div>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>IMD & NOAA Telemetry</span>
      </div>

      <div className="climate-indices">
        {/* ENSO Card */}
        <div className="climate-index-card">
          <div className="climate-index-label">ENSO (Niño 3.4)</div>
          <div className="climate-index-value" style={{
            color: ninoVal > 0.5 ? '#B91C1C' : ninoVal < -0.5 ? '#15803D' : '#1A1D2E'
          }}>
            {enso?.nino34 != null ? (ninoVal > 0 ? '+' : '') + ninoVal.toFixed(2) : '0.00'}°C
          </div>
          <div className={`climate-index-phase ${getPhaseClass(enso?.phase)}`}>
            {enso?.phase || 'Neutral'}
          </div>

          {/* Visual Gauge Bar */}
          <div className="gauge-bar-track" title={`Niño 3.4: ${ninoVal.toFixed(2)}°C`}>
            <div
              style={{
                position: 'absolute',
                left: `${ensoPercent}%`,
                top: '-3px',
                width: '14px',
                height: '14px',
                borderRadius: '50%',
                background: '#3B82F6',
                border: '2px solid #FFFFFF',
                boxShadow: '0 1px 4px rgba(0,0,0,0.3)',
                transform: 'translateX(-50%)',
              }}
            />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', fontSize: '0.68rem', color: 'var(--text-light)' }}>
            <span>La Niña (-2.5)</span>
            <span>Neutral</span>
            <span>El Niño (+2.5)</span>
          </div>
          <div className="climate-impact-text">{ensoImpact}</div>
        </div>

        {/* IOD Card */}
        <div className="climate-index-card">
          <div className="climate-index-label">IOD (DMI)</div>
          <div className="climate-index-value" style={{
            color: iodVal > 0.4 ? '#15803D' : iodVal < -0.4 ? '#B91C1C' : '#1A1D2E'
          }}>
            {iod?.dmi != null ? (iodVal > 0 ? '+' : '') + iodVal.toFixed(2) : '0.00'}
          </div>
          <div className={`climate-index-phase ${getPhaseClass(iod?.phase)}`}>
            {iod?.phase || 'Neutral'}
          </div>

          {/* Visual Gauge Bar */}
          <div className="gauge-bar-track" title={`DMI: ${iodVal.toFixed(2)}`}>
            <div
              style={{
                position: 'absolute',
                left: `${iodPercent}%`,
                top: '-3px',
                width: '14px',
                height: '14px',
                borderRadius: '50%',
                background: '#10B981',
                border: '2px solid #FFFFFF',
                boxShadow: '0 1px 4px rgba(0,0,0,0.3)',
                transform: 'translateX(-50%)',
              }}
            />
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', fontSize: '0.68rem', color: 'var(--text-light)' }}>
            <span>Negative (-1.0)</span>
            <span>Neutral</span>
            <span>Positive (+1.0)</span>
          </div>
          <div className="climate-impact-text">{iodImpact}</div>
        </div>

        {/* MJO Card */}
        <div className="climate-index-card">
          <div className="climate-index-label">MJO (RMM)</div>
          <div className="climate-index-value" style={{ color: '#7C3AED' }}>
            Phase {mjo?.phase || '3'}
          </div>
          <div className="climate-index-phase" style={{ background: '#F3E8FF', color: '#6B21A8', border: '1px solid #E9D5FF' }}>
            Amplitude: {mjo?.amplitude?.toFixed(1) || '1.3'}
          </div>

          {/* 8-Phase Pastel Indicator */}
          <div style={{ display: 'flex', gap: '3px', margin: '10px 0 6px', width: '100%' }}>
            {[1, 2, 3, 4, 5, 6, 7, 8].map((ph) => (
              <div
                key={ph}
                style={{
                  flex: 1,
                  height: '8px',
                  borderRadius: '3px',
                  background: ph === mjoPhase ? '#C9B8FF' : '#E2E4F0',
                  border: ph === mjoPhase ? '1px solid #9061F9' : 'none',
                }}
                title={`Phase ${ph}${ph === mjoPhase ? ' (Active)' : ''}`}
              />
            ))}
          </div>
          <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', fontSize: '0.68rem', color: 'var(--text-light)' }}>
            <span>P1 (Africa)</span>
            <span>P3 (Indian O.)</span>
            <span>P8 (Pacific)</span>
          </div>
          <div className="climate-impact-text">{mjoImpact}</div>
        </div>
      </div>
    </div>
  );
}
