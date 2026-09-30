/**
 * MonSense API Service Layer
 * Handles all HTTP requests to the FastAPI backend.
 */

const API_BASE = '/api/v1';

async function fetchAPI(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API call failed: ${endpoint}`, error);
    throw error;
  }
}

export const api = {
  // Dashboard
  getDashboardStats: () => fetchAPI('/dashboard/stats'),
  getRiskOverview: () => fetchAPI('/dashboard/risk-overview'),
  getRecentActivity: () => fetchAPI('/dashboard/recent-activity'),

  // Forecast
  getForecast: (locationCode, leadDays = 7) =>
    fetchAPI(`/forecast/predict/${locationCode}?lead_days=${leadDays}`),
  getTimeSeries: (locationCode, days = 30) =>
    fetchAPI(`/forecast/time-series/${locationCode}?days=${days}`),
  getRiskMap: (level = 'block', targetDate = null) => {
    let url = `/forecast/risk-map?level=${level}`;
    if (targetDate) url += `&target_date=${targetDate}`;
    return fetchAPI(url);
  },
  getDistrictSummary: (districtCode, days = 7) =>
    fetchAPI(`/forecast/summary/${districtCode}?days=${days}`),

  // Locations
  getLocations: (level = null) => {
    let url = '/locations/';
    if (level) url += `?level=${level}`;
    return fetchAPI(url);
  },
  getLocationHierarchy: () => fetchAPI('/locations/hierarchy'),
  getDistricts: () => fetchAPI('/locations/districts'),
  getBlocks: (districtId = null) => {
    let url = '/locations/blocks';
    if (districtId) url += `?district_id=${districtId}`;
    return fetchAPI(url);
  },
  searchLocations: (query) => fetchAPI(`/locations/search?q=${query}`),

  // Advisory
  getCrops: () => fetchAPI('/advisory/crops'),
  generateAdvisory: (locationCode, crops = 'rice,wheat,cotton,soybean', leadDays = 7) =>
    fetchAPI(`/advisory/generate/${locationCode}?crops=${crops}&lead_days=${leadDays}`),
  getBulkAdvisories: (districtCode, crops = 'rice,soybean', leadDays = 7) =>
    fetchAPI(`/advisory/bulk/${districtCode}?crops=${crops}&lead_days=${leadDays}`),

  // Alerts
  getFarmers: (locationId = null) => {
    let url = '/alerts/farmers';
    if (locationId) url += `?location_id=${locationId}`;
    return fetchAPI(url);
  },
  sendAlert: (phone, message, channel = 'sms', language = 'hi') =>
    fetchAPI(`/alerts/send?phone=${phone}&message=${encodeURIComponent(message)}&channel=${channel}&language=${language}`, { method: 'POST' }),
  broadcastAlert: (locationCode, channel = 'sms', crops = 'rice,soybean') =>
    fetchAPI(`/alerts/broadcast/${locationCode}?channel=${channel}&crops=${crops}`, { method: 'POST' }),
  getAlertStats: () => fetchAPI('/alerts/stats'),
  getRecentAlerts: (limit = 20) => fetchAPI(`/alerts/recent?limit=${limit}`),
};
