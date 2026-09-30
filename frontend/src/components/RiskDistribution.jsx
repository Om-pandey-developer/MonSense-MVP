/**
 * MonSense Risk Distribution Chart
 * Donut chart for block-level risk breakdown.
 */

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const RISK_COLORS = {
  very_high: '#ef4444',
  high: '#f97316',
  moderate: '#eab308',
  low: '#22c55e',
  very_low: '#06b6d4',
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
        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          {totalBlocks} blocks
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', padding: '20px 24px', gap: 24 }}>
        <div style={{ width: 160, height: 160 }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={45}
                outerRadius={70}
                paddingAngle={3}
                dataKey="value"
                stroke="none"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: 'rgba(15, 23, 42, 0.95)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: 12,
                  fontSize: '0.85rem',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 8 }}>
          {Object.entries(distribution).map(([key, count]) => (
            <div key={key} style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.85rem' }}>
              <div style={{
                width: 10, height: 10, borderRadius: 2,
                background: RISK_COLORS[key],
                flexShrink: 0,
              }} />
              <span style={{ color: 'var(--text-secondary)', flex: 1 }}>
                {RISK_LABELS[key]}
              </span>
              <span style={{ color: 'var(--text-primary)', fontWeight: 600, fontFamily: 'Outfit' }}>
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
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}
