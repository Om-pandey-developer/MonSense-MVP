/**
 * MonSense Climate Indices Widget
 * Displays ENSO, IOD, and MJO teleconnection indices.
 * — Dr. Aarav Sharma (Chief Climatologist)
 */

export default function ClimateWidget({ indices }) {
  if (!indices) return null;

  const { enso, iod, mjo } = indices;

  const getPhaseClass = (phase) => {
    if (!phase) return 'phase-neutral';
    const p = phase.toLowerCase();
    if (p.includes('positive') || p.includes('niño') || p.includes('el')) return 'phase-negative';
    if (p.includes('negative') || p.includes('niña') || p.includes('la')) return 'phase-positive';
    return 'phase-neutral';
  };

  return (
    <div className="glass-card-static">
      <div className="card-header">
        <div className="card-title">🌍 Climate Teleconnection Indices</div>
      </div>
      <div className="climate-indices">
        <div className="climate-index-card">
          <div className="climate-index-label">ENSO (Niño 3.4)</div>
          <div className="climate-index-value" style={{
            color: enso?.nino34 > 0.5 ? '#ef4444' : enso?.nino34 < -0.5 ? '#22c55e' : '#94a3b8'
          }}>
            {enso?.nino34 != null ? (enso.nino34 > 0 ? '+' : '') + enso.nino34.toFixed(2) : 'N/A'}°C
          </div>
          <div className={`climate-index-phase ${getPhaseClass(enso?.phase)}`}>
            {enso?.phase || 'Unknown'}
          </div>
        </div>

        <div className="climate-index-card">
          <div className="climate-index-label">IOD (DMI)</div>
          <div className="climate-index-value" style={{
            color: iod?.dmi > 0.4 ? '#22c55e' : iod?.dmi < -0.4 ? '#ef4444' : '#94a3b8'
          }}>
            {iod?.dmi != null ? (iod.dmi > 0 ? '+' : '') + iod.dmi.toFixed(2) : 'N/A'}
          </div>
          <div className={`climate-index-phase ${getPhaseClass(iod?.phase)}`}>
            {iod?.phase || 'Unknown'}
          </div>
        </div>

        <div className="climate-index-card">
          <div className="climate-index-label">MJO (RMM)</div>
          <div className="climate-index-value" style={{ color: '#c084fc' }}>
            Phase {mjo?.phase || '—'}
          </div>
          <div className="climate-index-phase phase-neutral">
            Amplitude: {mjo?.amplitude?.toFixed(1) || '—'}
          </div>
        </div>
      </div>
    </div>
  );
}
