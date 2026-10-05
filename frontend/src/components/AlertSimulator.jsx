/**
 * MonSense Visual Mobile Alert Simulator
 * Realistic smartphone mockup with multi-lingual alerts, animated gateway logs,
 * and live farmer delivery status tracking.
 * — Manish Tiwari & Sneha Kulkarni
 */

import { useState, useEffect, useRef } from 'react';
import { mockData } from '../services/mockData';

const MESSAGES = {
  mr: {
    langLabel: 'मराठी',
    sender: 'MH-AGRI-ALERT',
    badge: 'आपत्कालीन इशारा',
    title: 'मुसळधार पाऊस इशारा (७२ मिमी)',
    body: 'पुढील २४ ते ४८ तासांत बारामती व लगतच्या भागात मुसळधार पावसाची शक्यता आहे. सोयाबीन व कापूस पिकांमधील पाण्याचा त्वरित निचरा करा. कीटकनाशक फवारणी ३ दिवस पुढे ढकला.',
    action: 'मदत हेल्पलाइन: १८००-१८०-१५५१ (किसान कॉल सेंटर)',
  },
  hi: {
    langLabel: 'हिन्दी',
    sender: 'MH-AGRI-ALERT',
    badge: 'आपातकालीन चेतावनी',
    title: 'भारी बारिश अलर्ट (72mm)',
    body: 'अगले 24-48 घंटों में बारामती और आसपास भारी बारिश की संभावना। सोयाबीन व कपास खेतों में जल निकासी की व्यवस्था करें। कीटनाशक छिड़काव 3 दिनों के लिए स्थगित करें।',
    action: 'किसान हेल्पलाइन: 1800-180-1551 पर संपर्क करें',
  },
  en: {
    langLabel: 'English',
    sender: 'MH-AGRI-ALERT',
    badge: 'Emergency Alert',
    title: 'Heavy Rainfall Warning (72mm)',
    body: 'Heavy rainfall (>70mm) predicted in next 24-48 hrs across Baramati block. Open field drainage channels immediately. Postpone chemical spraying on soybean and cotton crops.',
    action: 'Kisan Call Centre Helpline: 1800-180-1551',
  },
};

export default function AlertSimulator({ districtName = 'Pune' }) {
  const [selectedLang, setSelectedLang] = useState('mr');
  const [isBroadcasting, setIsBroadcasting] = useState(false);
  const [progress, setProgress] = useState(100);
  const [activeTab, setActiveTab] = useState('whatsapp'); // 'whatsapp' | 'sms'
  const [logs, setLogs] = useState([
    '[SYSTEM] MonSense Rural Telecom Gateway v2.4 initialized',
    `[GEO] District polygon mapped: ${districtName} (4km mesh downscaling)`,
    '[STATUS] 8 registered demo farmers synchronized with Kisan Database',
    '[STANDBY] Ready for emergency broadcast simulation',
  ]);
  const [farmers, setFarmers] = useState([
    { id: 'f1', name: 'Ramesh Patil', phone: '+91 98231 45678', village: 'Malad', crop: 'Soybean', channel: 'SMS', status: 'Delivered' },
    { id: 'f2', name: 'Sunita Jadhav', phone: '+91 94220 78901', village: 'Supe', crop: 'WhatsApp', channel: 'WhatsApp', status: 'Delivered' },
    { id: 'f3', name: 'Ganesh Deshmukh', phone: '+91 98500 12345', village: 'Katewadi', crop: 'Rice', channel: 'SMS', status: 'Delivered' },
    { id: 'f4', name: 'Lakshmi Bhosale', phone: '+91 97632 99881', village: 'Baramati', crop: 'Cotton', channel: 'WhatsApp', status: 'Delivered' },
    { id: 'f5', name: 'Ashok More', phone: '+91 94033 44556', village: 'Indapur', crop: 'Soybean', channel: 'SMS', status: 'Delivered' },
    { id: 'f6', name: 'Pooja Kulkarni', phone: '+91 98902 33441', village: 'Junnar', crop: 'Vegetables', channel: 'WhatsApp', status: 'Delivered' },
    { id: 'f7', name: 'Dnyaneshwar Shinde', phone: '+91 98229 66778', village: 'Shirur', crop: 'Sugarcane', channel: 'SMS', status: 'Delivered' },
    { id: 'f8', name: 'Anand Gaikwad', phone: '+91 94211 88990', village: 'Haveli', crop: 'Wheat', channel: 'WhatsApp', status: 'Delivered' },
  ]);

  const terminalRef = useRef(null);

  useEffect(() => {
    if (terminalRef.current) {
      terminalRef.current.scrollTop = terminalRef.current.scrollHeight;
    }
  }, [logs]);

  const handleBroadcast = () => {
    setIsBroadcasting(true);
    setProgress(0);
    setLogs((prev) => [
      ...prev,
      `--- [BROADCAST INITIATED] Target: ${districtName} (${new Date().toLocaleTimeString()}) ---`,
      '[AUTH] Handshake with State Agriculture Department Gateway: Verified',
      '[ROUTING] Dispatching to BSNL, Jio, and Airtel Cell Broadcast Towers...',
    ]);

    // Reset farmers status to queued
    setFarmers((prev) => prev.map((f) => ({ ...f, status: 'Queued' })));

    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += 20;
      setProgress(currentProgress);

      const farmerIdx = Math.floor(currentProgress / 13);
      if (farmerIdx < farmers.length) {
        const farmer = farmers[farmerIdx];
        setLogs((prev) => [
          ...prev,
          `[DISPATCH] ${farmer.name} (${farmer.village}) -> ${farmer.channel} Ack 200 Delivered`,
        ]);
        setFarmers((prev) =>
          prev.map((f, i) => (i <= farmerIdx ? { ...f, status: 'Delivered' } : { ...f, status: 'Sending' }))
        );
      }

      if (currentProgress >= 100) {
        clearInterval(interval);
        setIsBroadcasting(false);
        setLogs((prev) => [
          ...prev,
          `[COMPLETE] 100% Broadcast delivered. 8/8 farmers reached successfully.`,
        ]);
        setFarmers((prev) => prev.map((f) => ({ ...f, status: 'Delivered' })));
      }
    }, 450);
  };

  const currentMsg = MESSAGES[selectedLang];

  return (
    <div className="glass-card-static" style={{ marginTop: 24 }}>
      <div className="card-header">
        <div className="card-title">
          📱 Multilingual Mobile Alert Dispatch Simulator
        </div>
        <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
          <button
            className="btn btn-coral"
            onClick={handleBroadcast}
            disabled={isBroadcasting}
          >
            {isBroadcasting ? '📡 Dispatching...' : '📡 Trigger Emergency Broadcast'}
          </button>
        </div>
      </div>

      <div className="card-body">
        {/* Progress Bar */}
        {isBroadcasting && (
          <div style={{ marginBottom: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', fontWeight: 600, marginBottom: 6 }}>
              <span>Cell Broadcast Dispatching to {districtName}...</span>
              <span>{progress}%</span>
            </div>
            <div style={{ height: 8, background: '#E2E4F0', borderRadius: 9999, overflow: 'hidden' }}>
              <div
                style={{
                  height: '100%',
                  width: `${progress}%`,
                  background: 'linear-gradient(90deg, #A8E6CF, #A3D5FF, #FFB3B3)',
                  transition: 'width 0.4s ease',
                }}
              />
            </div>
          </div>
        )}

        <div className="alert-simulator-layout">
          {/* Smartphone Mockup */}
          <div className="phone-mockup">
            <div className="phone-notch" />
            <div className="phone-screen">
              {/* Phone Status Bar */}
              <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 16px', fontSize: '0.7rem', color: '#7C7F9B', fontWeight: 600 }}>
                <span>10:30 AM</span>
                <span>📶 4G • 98% 🔋</span>
              </div>

              {/* Phone App Header */}
              <div className="phone-header">
                <div className="phone-avatar">
                  🌧️
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#1A1D2E' }}>
                    {currentMsg.sender}
                  </div>
                  <div style={{ fontSize: '0.7rem', color: '#15803D', fontWeight: 500 }}>
                    Official Government Channel • Verified
                  </div>
                </div>
              </div>

              {/* Channel Selector in Phone (WhatsApp / SMS) */}
              <div style={{ display: 'flex', borderBottom: '1px solid #E2E4F0', background: '#FFFFFF' }}>
                <button
                  style={{
                    flex: 1,
                    padding: '8px 0',
                    border: 'none',
                    background: activeTab === 'whatsapp' ? '#F4F6FB' : '#FFFFFF',
                    borderBottom: activeTab === 'whatsapp' ? '2px solid #25D366' : 'none',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    color: activeTab === 'whatsapp' ? '#1A1D2E' : '#7C7F9B',
                  }}
                  onClick={() => setActiveTab('whatsapp')}
                >
                  🟢 WhatsApp
                </button>
                <button
                  style={{
                    flex: 1,
                    padding: '8px 0',
                    border: 'none',
                    background: activeTab === 'sms' ? '#F4F6FB' : '#FFFFFF',
                    borderBottom: activeTab === 'sms' ? '2px solid #3B82F6' : 'none',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    color: activeTab === 'sms' ? '#1A1D2E' : '#7C7F9B',
                  }}
                  onClick={() => setActiveTab('sms')}
                >
                  💬 SMS Alert
                </button>
              </div>

              {/* Language Switcher Inside Phone */}
              <div style={{ padding: '8px 12px', background: '#FFFFFF', borderBottom: '1px solid #ECEEF8', display: 'flex', gap: 6, justifyContent: 'center' }}>
                {Object.entries(MESSAGES).map(([langKey, data]) => (
                  <button
                    key={langKey}
                    onClick={() => setSelectedLang(langKey)}
                    style={{
                      border: 'none',
                      background: selectedLang === langKey ? '#A3D5FF' : '#F0F1F8',
                      color: selectedLang === langKey ? '#0F3A66' : '#4A4E69',
                      padding: '3px 10px',
                      borderRadius: 12,
                      fontSize: '0.72rem',
                      fontWeight: 600,
                      cursor: 'pointer',
                    }}
                  >
                    {data.langLabel}
                  </button>
                ))}
              </div>

              {/* Chat Body */}
              <div className="phone-chat-body">
                <div style={{ textAlign: 'center', fontSize: '0.68rem', color: '#7C7F9B', margin: '4px 0' }}>
                  TODAY
                </div>

                <div className="chat-bubble inbound alert-high">
                  <div style={{ display: 'inline-block', background: '#FFD6D6', color: '#B91C1C', padding: '2px 8px', borderRadius: 4, fontSize: '0.68rem', fontWeight: 700, marginBottom: 6 }}>
                    🚨 {currentMsg.badge}
                  </div>
                  <div style={{ fontWeight: 700, fontSize: '0.85rem', marginBottom: 4, color: '#1A1D2E' }}>
                    {currentMsg.title}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#2D324D', lineHeight: 1.4 }}>
                    {currentMsg.body}
                  </div>
                  <div style={{ marginTop: 8, fontSize: '0.72rem', color: '#0369A1', background: '#E0F2FE', padding: '4px 8px', borderRadius: 6, fontWeight: 500 }}>
                    📞 {currentMsg.action}
                  </div>
                  <div className="chat-bubble-time">
                    10:30 AM • Delivered ✓✓
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column: Terminal Logs & Delivery Table */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {/* Live Gateway Terminal */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-dark)' }}>
                  💻 Telecom Dispatch Terminal Output
                </span>
                <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                  Simulated Gateway Logs
                </span>
              </div>
              <div className="simulator-terminal" ref={terminalRef}>
                {logs.map((log, index) => {
                  let cls = '';
                  if (log.includes('Delivered') || log.includes('COMPLETE') || log.includes('Verified')) cls = 'success';
                  else if (log.includes('BROADCAST') || log.includes('Warning')) cls = 'warning';
                  else if (log.includes('FAILED')) cls = 'error';
                  return (
                    <div key={index} className={`terminal-line ${cls}`}>
                      {log}
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Live Farmer Dispatch Status */}
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-dark)' }}>
                  👨‍🌾 Targeted Farmers Broadcast Status
                </span>
                <span style={{ fontSize: '0.75rem', color: '#15803D', fontWeight: 600 }}>
                  8 / 8 Active
                </span>
              </div>
              <div style={{ maxHeight: 240, overflowY: 'auto', border: '1px solid var(--pastel-border)', borderRadius: 12 }}>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Farmer</th>
                      <th>Village</th>
                      <th>Crop</th>
                      <th>Channel</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {farmers.map((f) => (
                      <tr key={f.id}>
                        <td style={{ fontWeight: 600, color: 'var(--text-dark)' }}>{f.name}</td>
                        <td>{f.village}</td>
                        <td>{f.crop}</td>
                        <td>
                          <span style={{
                            padding: '2px 8px',
                            borderRadius: 6,
                            fontSize: '0.72rem',
                            fontWeight: 600,
                            background: f.channel === 'WhatsApp' ? '#DCFCE7' : '#E0F2FE',
                            color: f.channel === 'WhatsApp' ? '#15803D' : '#0369A1',
                          }}>
                            {f.channel}
                          </span>
                        </td>
                        <td>
                          <span className={`risk-badge ${f.status === 'Delivered' ? 'low' : f.status === 'Sending' ? 'moderate' : 'very-low'}`}>
                            {f.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
