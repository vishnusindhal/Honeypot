/**
 * API Service for Honeypot Dashboard
 * Fetches real data from the Flask API server
 */

const API_BASE_URL = 'http://localhost:5000/api';

async function fetchWithFallback(url, fallbackData) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('API error');
    return await response.json();
  } catch (error) {
    console.warn(`API call to ${url} failed, using fallback data:`, error);
    return fallbackData;
  }
}

// Fallback data (used when API is not available)
const fallbackMetrics = {
  activeSessions: 0,
  totalCommands: 0,
  highRiskActions: 0,
  avgSessionDuration: "0m 0s"
};

const fallbackSessions = [];
const fallbackCommands = [];

export const api = {
  // Health check
  async checkHealth() {
    return fetchWithFallback(`${API_BASE_URL}/health`, { status: 'offline' });
  },

  // Get dashboard metrics
  async getMetrics() {
    return fetchWithFallback(`${API_BASE_URL}/metrics`, fallbackMetrics);
  },

  // Get all sessions
  async getSessions() {
    return fetchWithFallback(`${API_BASE_URL}/sessions`, fallbackSessions);
  },

  // Get all commands
  async getCommands() {
    return fetchWithFallback(`${API_BASE_URL}/commands`, fallbackCommands);
  },

  // Get command frequency for charts
  async getCommandFrequency() {
    return fetchWithFallback(`${API_BASE_URL}/commands/frequency`, []);
  },

  // Get risk distribution for charts
  async getRiskDistribution() {
    return fetchWithFallback(`${API_BASE_URL}/analytics/risk-distribution`, [
      { name: "Critical", value: 0, color: "#ef4444" },
      { name: "High", value: 0, color: "#f97316" },
      { name: "Medium", value: 0, color: "#eab308" },
      { name: "Low", value: 0, color: "#22c55e" }
    ]);
  },

  // Get skill distribution for heatmap
  async getSkillDistribution() {
    return fetchWithFallback(`${API_BASE_URL}/analytics/skill-distribution`, [
      { name: "High", value: 0, color: "#ef4444" },
      { name: "Medium", value: 0, color: "#f97316" },
      { name: "Low", value: 0, color: "#22c55e" }
    ]);
  },

  // Get timeline data for charts
  async getTimeline() {
    return fetchWithFallback(`${API_BASE_URL}/analytics/timeline`, []);
  },

  // Get session replay data
  async getSessionReplay(sessionId) {
    return fetchWithFallback(`${API_BASE_URL}/session/${sessionId}/replay`, []);
  },

  // Get session recordings
  async getRecordings() {
    return fetchWithFallback(`${API_BASE_URL}/recordings`, []);
  }
};

export default api;
