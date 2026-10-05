/**
 * MonSense Risk Distribution Chart
 * Donut chart for block-level risk breakdown in soft pastel palette.
 */

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

export const RISK_COLORS = {
  very_high: '#FF8A8A',
  high: '#FFB3B3',
  moderate: '#FFE0A3',
  low: '#A8E6CF',
  very_low: '#A3D5FF',
};

const RISK_LABELS = {
  very_high: 'Very High',
  high: 'High',
  moderate: 'Moderate',
  low: 'Low',
  very_low: 'Very Low',
};

export default function RiskDistribution({ distribution, totalBlocks }) {
  if (!distribution) return null;

  const data = Object.entries(distribution)
    .filter(([, value]) => value > 0)
    .map(([key, value]) => ({
      name: RISK_LABELS[key],
      value,
      color: RISK_COLORS[key],
    }));

  if (data.length === 0) return null;

  return (
    <div className="glass-card-static">
      <div className="card-header">
        <div className="card-title">📊 Risk Distribution</div>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 500 }}>
          {totalBlocks} blocks
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', padding: '20px 24px', gap: 24, flexWrap: 'wrap' }}>
        <div style={{ width: 160, height: 160, margin: '0 auto' }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={45}
                outerRadius={70}
                paddingAngle={4}
                dataKey="value"
                stroke="#FFFFFF"
                strokeWidth={2}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: '#FFFFFF',
                  border: '1px solid #E2E4F0',
                  borderRadius: 10,
                  fontSize: '0.85rem',
                  boxShadow: '0 4px 12px rgba(26,29,46,0.08)',
                  color: '#1A1D2E',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div style={{ flex: 1, minWidth: '150px', display: 'flex', flexDirection: 'column', gap: 8 }}>
          {Object.entries(distribution).map(([key, count]) => (
            <div key={key} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem' }}>
              <div style={{
                width: 12, height: 12, borderRadius: 3,
                background: RISK_COLORS[key],
                border: '1px solid rgba(0,0,0,0.08)',
                flexShrink: 0,
              }} />
              <span style={{ color: 'var(--text-secondary)', flex: 1 }}>
                {RISK_LABELS[key]}
              </span>
              <span style={{ color: 'var(--text-dark)', fontWeight: 700, fontFamily: 'Outfit' }}>
                {count}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Risk bar */}
      <div style={{ padding: '0 24px 20px' }}>
        <div className="risk-bar">
          {Object.entries(distribution).map(([key, count]) => {
            const total = Object.values(distribution).reduce((a, b) => a + b, 0);
            const pct = total > 0 ? (count / total) * 100 : 0;
            return (
              <div
                key={key}
                className="risk-bar-segment"
                style={{
                  width: `${pct}%`,
                  background: RISK_COLORS[key],
                }}
                title={`${RISK_LABELS[key]}: ${count} (${Math.round(pct)}%)`}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}
