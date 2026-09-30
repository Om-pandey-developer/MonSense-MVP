/**
 * MonSense — Mock Data Provider
 * Provides realistic demo data when backend is not running.
 * — Ensures the frontend works standalone for hackathon demo.
 */

function seededRandom(seed) {
  let s = seed;
  return function () {
    s = (s * 16807) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

const MONTHS_CLIMATOLOGY = {
  1: 2, 2: 3, 3: 5, 4: 8, 5: 15, 6: 45,
  7: 65, 8: 55, 9: 40, 10: 20, 11: 8, 12: 3,
};

function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash |= 0;
  }
  return Math.abs(hash);
}

function generateForecast(locationCode, targetDate, leadDays) {
  const seed = hashCode(`${locationCode}_${targetDate}`);
  const rng = seededRandom(seed);

  const d = new Date(targetDate);
  const month = d.getMonth() + 1;
  const base = MONTHS_CLIMATOLOGY[month] || 10;

  const rainfall = Math.max(0, base * (0.5 + rng() * 1.2));
  const heavyProb = Math.min(100, Math.max(0, (rainfall / (base * 2)) * 60 + (rng() - 0.5) * 20));
  const dryProb = Math.min(100, Math.max(0, 100 - (rainfall / base) * 80 + (rng() - 0.5) * 15));
  const floodProb = Math.min(100, Math.max(0, heavyProb * 0.7 + rng() * 20));
  const monsoonProb = (month >= 5 && month <= 7) ? Math.max(0, 70 - Math.abs(160 - (d.getDate() + month * 30)) * 2) : 0;

  const maxProb = Math.max(heavyProb, floodProb);
  let risk;
  if (maxProb >= 70) risk = 'very_high';
  else if (maxProb >= 50) risk = 'high';
  else if (maxProb >= 30) risk = 'moderate';
  else if (maxProb >= 10) risk = 'low';
  else risk = 'very_low';

  return {
    predicted_rainfall_mm: Math.round(rainfall * 10) / 10,
    rainfall_lower_bound: Math.round(Math.max(0, rainfall - rainfall * 0.3) * 10) / 10,
    rainfall_upper_bound: Math.round((rainfall + rainfall * 0.3) * 10) / 10,
    prediction_confidence: Math.round((0.85 - leadDays * 0.015) * 1000) / 1000,
    heavy_rainfall_prob: Math.round(heavyProb * 10) / 10,
    dry_spell_prob: Math.round(dryProb * 10) / 10,
    monsoon_onset_prob: Math.round(monsoonProb * 10) / 10,
    flood_risk_prob: Math.round(floodProb * 10) / 10,
    risk_category: risk,
    model_version: '1.0.0-demo',
    model_type: 'LSTM+XGBoost Ensemble',
    target_date: targetDate,
    lead_days: leadDays,
  };
}

const LOCATIONS = {
  districts: [
    { id: 'b0000001-0000-0000-0000-000000000001', name: 'Pune', name_local: 'पुणे', code: 'MH-PUN', level: 'district', latitude: 18.5204, longitude: 73.8567, elevation_m: 560 },
    { id: 'b0000002-0000-0000-0000-000000000001', name: 'Nagpur', name_local: 'नागपूर', code: 'MH-NAG', level: 'district', latitude: 21.1458, longitude: 79.0882, elevation_m: 310 },
    { id: 'b0000003-0000-0000-0000-000000000001', name: 'Nashik', name_local: 'नाशिक', code: 'MH-NAS', level: 'district', latitude: 20.0, longitude: 73.78, elevation_m: 700 },
    { id: 'b0000004-0000-0000-0000-000000000001', name: 'Aurangabad', name_local: 'औरंगाबाद', code: 'MH-AUR', level: 'district', latitude: 19.8762, longitude: 75.3433, elevation_m: 570 },
    { id: 'b0000005-0000-0000-0000-000000000001', name: 'Kolhapur', name_local: 'कोल्हापूर', code: 'MH-KOL', level: 'district', latitude: 16.705, longitude: 74.2433, elevation_m: 569 },
    { id: 'b0000006-0000-0000-0000-000000000001', name: 'Solapur', name_local: 'सोलापूर', code: 'MH-SOL', level: 'district', latitude: 17.6599, longitude: 75.9064, elevation_m: 458 },
    { id: 'b0000007-0000-0000-0000-000000000001', name: 'Satara', name_local: 'सातारा', code: 'MH-SAT', level: 'district', latitude: 17.6805, longitude: 74.0183, elevation_m: 750 },
    { id: 'b0000008-0000-0000-0000-000000000001', name: 'Ahmednagar', name_local: 'अहमदनगर', code: 'MH-AHM', level: 'district', latitude: 19.0948, longitude: 74.748, elevation_m: 649 },
  ],
  blocks: [
    { id: 'c0000001-0000-0000-0000-000000000001', name: 'Baramati', code: 'MH-PUN-BAR', level: 'block', parent_id: 'b0000001-0000-0000-0000-000000000001', latitude: 18.1514, longitude: 74.5777, elevation_m: 550 },
    { id: 'c0000002-0000-0000-0000-000000000001', name: 'Indapur', code: 'MH-PUN-IND', level: 'block', parent_id: 'b0000001-0000-0000-0000-000000000001', latitude: 18.113, longitude: 75.0237, elevation_m: 500 },
    { id: 'c0000003-0000-0000-0000-000000000001', name: 'Junnar', code: 'MH-PUN-JUN', level: 'block', parent_id: 'b0000001-0000-0000-0000-000000000001', latitude: 19.2079, longitude: 73.8749, elevation_m: 720 },
    { id: 'c0000004-0000-0000-0000-000000000001', name: 'Haveli', code: 'MH-PUN-HAV', level: 'block', parent_id: 'b0000001-0000-0000-0000-000000000001', latitude: 18.5, longitude: 73.85, elevation_m: 580 },
    { id: 'c0000005-0000-0000-0000-000000000001', name: 'Mulshi', code: 'MH-PUN-MUL', level: 'block', parent_id: 'b0000001-0000-0000-0000-000000000001', latitude: 18.53, longitude: 73.51, elevation_m: 900 },
    { id: 'c0000006-0000-0000-0000-000000000001', name: 'Shirur', code: 'MH-PUN-SHR', level: 'block', parent_id: 'b0000001-0000-0000-0000-000000000001', latitude: 18.83, longitude: 74.37, elevation_m: 510 },
    { id: 'c0000007-0000-0000-0000-000000000001', name: 'Nagpur Rural', code: 'MH-NAG-RUR', level: 'block', parent_id: 'b0000002-0000-0000-0000-000000000001', latitude: 21.15, longitude: 79.05, elevation_m: 310 },
    { id: 'c0000008-0000-0000-0000-000000000001', name: 'Kamptee', code: 'MH-NAG-KAM', level: 'block', parent_id: 'b0000002-0000-0000-0000-000000000001', latitude: 21.23, longitude: 79.2, elevation_m: 290 },
    { id: 'c0000009-0000-0000-0000-000000000001', name: 'Igatpuri', code: 'MH-NAS-IGT', level: 'block', parent_id: 'b0000003-0000-0000-0000-000000000001', latitude: 19.69, longitude: 73.56, elevation_m: 900 },
    { id: 'c0000010-0000-0000-0000-000000000001', name: 'Malegaon', code: 'MH-NAS-MAL', level: 'block', parent_id: 'b0000003-0000-0000-0000-000000000001', latitude: 20.55, longitude: 74.53, elevation_m: 480 },
  ],
};

function today() {
  return new Date().toISOString().split('T')[0];
}

function dateAdd(days) {
  const d = new Date();
  d.setDate(d.getDate() + days);
  return d.toISOString().split('T')[0];
}

export const mockData = {
  getDashboardStats: () => {
    const month = new Date().getMonth() + 1;
    let monsoon;
    if (month >= 6 && month <= 9) monsoon = 'active';
    else if (month === 5) monsoon = 'onset';
    else if (month === 10) monsoon = 'retreat';
    else monsoon = 'off-season';

    return {
      total_locations: 23,
      total_districts: 8,
      total_blocks: 10,
      total_villages: 3,
      registered_farmers: 5,
      active_forecasts: 10,
      active_advisories: 7,
      alerts_sent_today: 12,
      high_risk_blocks: 3,
      monsoon_status: monsoon,
      climate_indices: {
        enso: { nino34: -0.42, phase: 'Neutral' },
        iod: { dmi: 0.31, phase: 'Neutral' },
        mjo: { phase: 5, amplitude: 1.3 },
      },
    };
  },

  getRiskOverview: () => {
    const blocks = LOCATIONS.blocks.map((b) => {
      const forecast = generateForecast(b.code, dateAdd(7), 7);
      return {
        name: b.name,
        code: b.code,
        risk: forecast.risk_category,
        rainfall_mm: forecast.predicted_rainfall_mm,
        heavy_prob: forecast.heavy_rainfall_prob,
      };
    });

    const distribution = { very_low: 0, low: 0, moderate: 0, high: 0, very_high: 0 };
    blocks.forEach((b) => { distribution[b.risk]++; });

    blocks.sort((a, b2) => {
      const order = { very_high: 0, high: 1, moderate: 2, low: 3, very_low: 4 };
      return order[a.risk] - order[b2.risk];
    });

    return { target_date: dateAdd(7), distribution, blocks };
  },

  getRiskMap: () => {
    const features = LOCATIONS.blocks.map((b) => {
      const forecast = generateForecast(b.code, dateAdd(7), 7);
      const delta = 0.15;
      return {
        type: 'Feature',
        properties: {
          location_id: b.id,
          location_name: b.name,
          location_code: b.code,
          rainfall_mm: forecast.predicted_rainfall_mm,
          heavy_rainfall_prob: forecast.heavy_rainfall_prob,
          dry_spell_prob: forecast.dry_spell_prob,
          flood_risk_prob: forecast.flood_risk_prob,
          risk_category: forecast.risk_category,
          target_date: dateAdd(7),
          confidence: forecast.prediction_confidence,
        },
        geometry: {
          type: 'Polygon',
          coordinates: [[
            [b.longitude - delta, b.latitude - delta],
            [b.longitude + delta, b.latitude - delta],
            [b.longitude + delta, b.latitude + delta],
            [b.longitude - delta, b.latitude + delta],
            [b.longitude - delta, b.latitude - delta],
          ]],
        },
      };
    });

    const riskCounts = { very_low: 0, low: 0, moderate: 0, high: 0, very_high: 0 };
    features.forEach((f) => { riskCounts[f.properties.risk_category]++; });

    return {
      type: 'FeatureCollection',
      features,
      metadata: {
        target_date: dateAdd(7),
        level: 'block',
        total_locations: features.length,
        risk_distribution: riskCounts,
      },
    };
  },

  getTimeSeries: (locationCode) => {
    const data = [];
    for (let i = 0; i < 30; i++) {
      const targetDate = dateAdd(i);
      const forecast = generateForecast(locationCode, targetDate, i + 1);
      data.push({
        ...forecast,
        target_date: targetDate,
        lead_days: i + 1,
      });
    }
    return {
      location: { name: locationCode.split('-').pop(), code: locationCode },
      parameter: 'rainfall',
      unit: 'mm/day',
      forecast_start: today(),
      data,
    };
  },

  getAdvisories: (locationCode) => {
    const forecast = generateForecast(locationCode, dateAdd(7), 7);
    const advisories = [];

    if (forecast.heavy_rainfall_prob > 50) {
      advisories.push({
        crop_name: 'Rice',
        crop_stage: 'vegetative',
        advisory_type: 'drain_fields',
        advisory_text_en: `🚿 DRAIN FIELDS: Very heavy rainfall (${forecast.predicted_rainfall_mm}mm) expected. Ensure proper drainage for Rice. Risk of waterlogging and root damage.`,
        advisory_text_hi: `🚿 खेत से पानी निकालें: बहुत भारी बारिश (${forecast.predicted_rainfall_mm}mm) का अनुमान। धान के लिए उचित जल निकासी सुनिश्चित करें।`,
        severity: 'warning',
        actions: { primary: 'Create drainage channels', secondary: 'Raise bunds around low-lying areas' },
      });
    }

    if (forecast.dry_spell_prob > 40) {
      advisories.push({
        crop_name: 'Soybean',
        crop_stage: 'flowering',
        advisory_type: 'arrange_irrigation',
        advisory_text_en: `💧 ARRANGE IRRIGATION: Dry spell expected. Only ${forecast.predicted_rainfall_mm}mm rain forecast. Soybean at flowering stage needs supplemental irrigation.`,
        advisory_text_hi: `💧 सिंचाई की व्यवस्था करें: सूखे का अनुमान। केवल ${forecast.predicted_rainfall_mm}mm बारिश का पूर्वानुमान।`,
        severity: 'warning',
        actions: { primary: 'Arrange supplemental irrigation', secondary: 'Apply mulch' },
      });
    }

    advisories.push({
      crop_name: 'Cotton',
      crop_stage: 'vegetative',
      advisory_type: 'apply_fungicide',
      advisory_text_en: '🧪 APPLY FUNGICIDE: Prolonged wet conditions expected. Cotton at vegetative stage is vulnerable to fungal diseases.',
      advisory_text_hi: '🧪 कवकनाशी छिड़काव करें: लंबे समय तक गीली परिस्थितियों का अनुमान। कपास कवक रोगों के प्रति संवेदनशील।',
      severity: 'info',
      actions: { primary: 'Apply recommended fungicide', secondary: 'Ensure spacing for air circulation' },
    });

    if (forecast.flood_risk_prob > 50) {
      advisories.push({
        crop_name: 'All Crops',
        crop_stage: 'all',
        advisory_type: 'flood_warning',
        advisory_text_en: `⚠️ FLOOD WARNING: ${Math.round(forecast.flood_risk_prob)}% flood risk in your area. Move livestock and stored grain to higher ground.`,
        advisory_text_hi: `⚠️ बाढ़ चेतावनी: ${Math.round(forecast.flood_risk_prob)}% बाढ़ का खतरा। पशुधन और अनाज को ऊँचे स्थान पर ले जाएँ।`,
        severity: 'critical',
        actions: { primary: 'Move livestock to safety', secondary: 'Reinforce bunds' },
      });
    }

    return {
      location: { name: locationCode.split('-').pop() || 'Baramati', code: locationCode },
      forecast_summary: {
        target_date: dateAdd(7),
        predicted_rainfall_mm: forecast.predicted_rainfall_mm,
        risk_category: forecast.risk_category,
        heavy_rainfall_prob: forecast.heavy_rainfall_prob,
        dry_spell_prob: forecast.dry_spell_prob,
      },
      total_advisories: advisories.length,
      advisories,
    };
  },

  getDistricts: () => ({
    total: LOCATIONS.districts.length,
    districts: LOCATIONS.districts,
  }),

  getBlocks: () => ({
    total: LOCATIONS.blocks.length,
    blocks: LOCATIONS.blocks,
  }),

  getFarmers: () => ({
    total: 5,
    farmers: [
      { id: 'f1', name: 'Ramesh Patil', phone: '+919876543210', crops: ['soybean', 'cotton'], language_preference: 'hi' },
      { id: 'f2', name: 'Sunita Jadhav', phone: '+919876543211', crops: ['sugarcane', 'rice'], language_preference: 'hi' },
      { id: 'f3', name: 'Ganesh Deshmukh', phone: '+919876543212', crops: ['wheat', 'groundnut'], language_preference: 'hi' },
      { id: 'f4', name: 'Lakshmi Bhosale', phone: '+919876543213', crops: ['rice', 'pulses'], language_preference: 'hi' },
      { id: 'f5', name: 'Ashok More', phone: '+919876543214', crops: ['cotton', 'soybean', 'maize'], language_preference: 'hi' },
    ],
  }),

  getAlertStats: () => ({
    total_alerts: 47,
    sms_sent: 32,
    whatsapp_sent: 15,
    delivered: 44,
    failed: 3,
    delivery_rate: '93.6%',
  }),
};
