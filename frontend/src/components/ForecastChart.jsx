/**
 * MonSense Forecast Chart Component
 * Rainfall time-series with Recharts styled in pastel tones.
 */

import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts';

const RISK_COLORS = {
  very_high: '#FF8A8A',
  high: '#FFB3B3',
  moderate: '#FFE0A3',
  low: '#A8E6CF',
  very_low: '#A3D5FF',
};

const CustomTooltip = ({ active, payload }) => {
  if (!active || !payload || !payload.length) return null;

  const data = payload[0].payload;
  const riskColor = RISK_COLORS[data.risk_category] || '#A3D5FF';

  return (
    <div style={{
      background: '#FFFFFF',
      border: '1px solid #E2E4F0',
      borderRadius: '12px',
      padding: '14px 18px',
      boxShadow: '0 8px 24px rgba(26, 29, 46, 0.08)',
      minWidth: '190px',
    }}>
      <div style={{ fontFamily: 'Outfit', fontWeight: 700, marginBottom: 8, color: '#1A1D2E' }}>
        {data.target_date}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#4A4E69', marginBottom: 4 }}>
        <span>Rainfall</span>
        <span style={{ color: '#2563EB', fontWeight: 700 }}>{data.predicted_rainfall_mm} mm</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#4A4E69', marginBottom: 4 }}>
        <span>Heavy Rain</span>
        <span style={{ color: '#D97706', fontWeight: 600 }}>{Math.round(data.heavy_rainfall_prob)}%</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', color: '#4A4E69', marginBottom: 4 }}>
        <span>Dry Spell</span>
        <span style={{ color: '#B45309', fontWeight: 600 }}>{Math.round(data.dry_spell_prob)}%</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem', color: '#4A4E69', marginTop: 6, paddingTop: 6, borderTop: '1px solid #F0F1F8' }}>
        <span>Risk Category</span>
        <span style={{
          fontWeight: 700,
          textTransform: 'uppercase',
          fontSize: '0.72rem',
          padding: '2px 8px',
          borderRadius: '9999px',
          background: riskColor,
          color: '#1A1D2E',
        }}>
          {data.risk_category?.replace('_', ' ')}
        </span>
      </div>
    </div>
  );
};

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
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 500 }}>
          LSTM + XGBoost Downscaled
        </span>
      </div>
      <div className="chart-container">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 20, bottom: 0, left: 0 }}>
            <defs>
              <linearGradient id="rainfallGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#A3D5FF" stopOpacity={0.7} />
                <stop offset="95%" stopColor="#A3D5FF" stopOpacity={0.05} />
              </linearGradient>
              <linearGradient id="upperGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#FFE0A3" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#FFE0A3" stopOpacity={0.02} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#ECEEF8" vertical={false} />
            <XAxis
              dataKey="dateLabel"
              tick={{ fontSize: 11, fill: '#7C7F9B' }}
              tickLine={false}
              axisLine={{ stroke: '#E2E4F0' }}
              interval={4}
            />
            <YAxis
              tick={{ fontSize: 11, fill: '#7C7F9B' }}
              tickLine={false}
              axisLine={false}
              label={{ value: 'mm/day', angle: -90, position: 'insideLeft', fill: '#7C7F9B', fontSize: 11 }}
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
              stroke="#3B82F6"
              strokeWidth={2.5}
              fill="url(#rainfallGrad)"
              name="Predicted Rainfall"
              dot={false}
              activeDot={{ r: 5, fill: '#3B82F6', stroke: '#FFFFFF', strokeWidth: 2 }}
            />
            <Area
              type="monotone"
              dataKey="rainfall_lower_bound"
              stroke="transparent"
              fill="transparent"
              name="Lower Bound"
            />
            <ReferenceLine
              y={50}
              stroke="#FF8A8A"
              strokeDasharray="4 4"
              strokeWidth={1.5}
              label={{ value: 'Heavy Rain (50mm)', fill: '#D32F2F', fontSize: 10, position: 'top' }}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
