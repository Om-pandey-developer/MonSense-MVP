/**
 * MonSense Forecast Chart Component
 * Rainfall time-series with Recharts.
 * — Sneha Kulkarni (Frontend UI/UX)
 */

import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload || !payload.length) return null;

  const data = payload[0].payload;
  return (
    <div style={{
      background: 'rgba(15, 23, 42, 0.95)',
      border: '1px solid rgba(255,255,255,0.1)',
      borderRadius: '12px',
      padding: '14px 18px',
      backdropFilter: 'blur(20px)',
      minWidth: '180px',
    }}>
      <div style={{ fontFamily: 'Outfit', fontWeight: 600, marginBottom: 8, color: '#f1f5f9' }}>
        {data.target_date}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#94a3b8', marginBottom: 4 }}>
        <span>Rainfall</span>
        <span style={{ color: '#38bdf8', fontWeight: 600 }}>{data.predicted_rainfall_mm} mm</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#94a3b8', marginBottom: 4 }}>
        <span>Heavy Rain</span>
        <span style={{ color: '#f97316', fontWeight: 600 }}>{Math.round(data.heavy_rainfall_prob)}%</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#94a3b8', marginBottom: 4 }}>
        <span>Dry Spell</span>
        <span style={{ color: '#eab308', fontWeight: 600 }}>{Math.round(data.dry_spell_prob)}%</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#94a3b8' }}>
        <span>Risk</span>
        <span style={{ fontWeight: 600, textTransform: 'uppercase', fontSize: '0.75rem', color: getRiskColor(data.risk_category) }}>
          {data.risk_category?.replace('_', ' ')}
        </span>
      </div>
    </div>
  );
};

function getRiskColor(risk) {
  const colors = {
    very_high: '#ef4444', high: '#f97316', moderate: '#eab308',
    low: '#22c55e', very_low: '#06b6d4',
  };
  return colors[risk] || '#64748b';
}

export default function ForecastChart({ data, locationName }) {
  if (!data || data.length === 0) {
    return (
      <div className="glass-card-static">
        <div className="card-header">
          <div className="card-title">📈 30-Day Rainfall Forecast</div>
        </div>
        <div className="chart-container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)' }}>
          No data available
        </div>
      </div>
    );
  }

  // Format dates for x-axis
  const chartData = data.map((d) => ({
    ...d,
    dateLabel: new Date(d.target_date).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }),
  }));

  return (
    <div className="glass-card-static">
      <div className="card-header">
        <div className="card-title">
          📈 30-Day Rainfall Forecast — {locationName || 'Selected Block'}
        </div>
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 20, bottom: 0, left: 0 }}>
            <defs>
              <linearGradient id="rainfallGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="upperGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f97316" stopOpacity={0.15} />
                <stop offset="95%" stopColor="#f97316" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
            <XAxis
              dataKey="dateLabel"
              tick={{ fontSize: 11, fill: '#64748b' }}
              tickLine={false}
              interval={4}
            />
            <YAxis
              tick={{ fontSize: 11, fill: '#64748b' }}
              tickLine={false}
              axisLine={false}
              label={{ value: 'mm/day', angle: -90, position: 'insideLeft', fill: '#64748b', fontSize: 11 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area
              type="monotone"
              dataKey="rainfall_upper_bound"
              stroke="transparent"
              fill="url(#upperGrad)"
              name="Upper Bound"
            />
            <Area
              type="monotone"
              dataKey="predicted_rainfall_mm"
              stroke="#38bdf8"
              strokeWidth={2}
              fill="url(#rainfallGrad)"
              name="Predicted Rainfall"
              dot={false}
              activeDot={{ r: 5, fill: '#38bdf8', stroke: '#0a0e17', strokeWidth: 2 }}
            />
            <Area
              type="monotone"
              dataKey="rainfall_lower_bound"
              stroke="transparent"
              fill="transparent"
              name="Lower Bound"
            />
            <ReferenceLine y={50} stroke="#ef4444" strokeDasharray="3 3" label={{ value: 'Heavy Rain Threshold', fill: '#ef4444', fontSize: 10 }} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
