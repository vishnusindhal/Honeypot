/**
 * ThreatMap Page — GeoIP Attacker Location Mapping
 * =================================================
 * 
 * Displays a world map with red markers showing where attackers are located.
 * Uses React Leaflet for the interactive map with dark-themed tiles.
 * 
 * Features:
 * - World map with zoom controls
 * - Red circle markers for each attacker IP
 * - Marker size scales with command count (more commands = bigger dot)
 * - Click popup shows IP, country, city, attack type, timestamp
 * - Auto-refreshes every 15 seconds for live data
 * - Summary stats bar at the top
 * 
 * Data Flow:
 *   1. Frontend calls GET /api/attacks/geo
 *   2. Backend reads honeypot_audit.json, extracts unique IPs
 *   3. Each IP is resolved via geoip_resolver.py (GeoLite2 or demo data)
 *   4. Frontend plots markers at returned lat/lng coordinates
 */

import { useState, useEffect } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup, useMap } from 'react-leaflet'
import { Globe, Crosshair, AlertTriangle, Activity, RefreshCw } from 'lucide-react'
import api from '../services/api'

// =========================================================================
// MAP CONFIGURATION
// =========================================================================

// Default map view: centered on the world
const MAP_CENTER = [20, 0]  // latitude, longitude
const MAP_ZOOM = 2          // zoom level (2 = whole world visible)

// Dark-themed map tiles (matches our dark dashboard)
const DARK_TILE_URL = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png'
const TILE_ATTRIBUTION = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>'

// =========================================================================
// HELPER: Color based on skill level
// =========================================================================
function getMarkerColor(skillLevel) {
  switch (skillLevel) {
    case 'High':   return '#ef4444'  // Red — dangerous
    case 'Medium': return '#f97316'  // Orange — moderate threat
    case 'Low':    return '#22c55e'  // Green — low threat
    default:       return '#06b6d4'  // Cyan — unknown
  }
}

// =========================================================================
// HELPER: Marker radius based on command count
// =========================================================================
function getMarkerRadius(commandCount) {
  // Scale: minimum 6px, maximum 20px
  const base = 6
  const scale = Math.min(commandCount / 5, 14)  // Max bonus = 14
  return base + scale
}

// =========================================================================
// SUB-COMPONENT: Map auto-refresh handler
// =========================================================================
function MapRefreshHandler({ data }) {
  const map = useMap()
  // This component exists inside MapContainer to access map instance
  // We could use it to fly to specific locations or auto-fit bounds
  return null
}

// =========================================================================
// SUB-COMPONENT: Summary Stats Bar
// =========================================================================
function StatsBar({ attacks }) {
  const totalAttacks = attacks.length
  const uniqueCountries = new Set(attacks.map(a => a.country)).size
  const highRisk = attacks.filter(a => a.skillLevel === 'High').length
  const totalCommands = attacks.reduce((sum, a) => sum + a.commandCount, 0)

  const stats = [
    { icon: Globe,          label: 'Countries',      value: uniqueCountries, color: 'text-cyan-400' },
    { icon: Crosshair,      label: 'Attacker IPs',   value: totalAttacks,    color: 'text-purple-400' },
    { icon: AlertTriangle,  label: 'High Risk',      value: highRisk,        color: 'text-red-400' },
    { icon: Activity,       label: 'Commands',        value: totalCommands,   color: 'text-green-400' },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {stats.map((stat, i) => (
        <div key={i} className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-4 flex items-center gap-3">
          <div className={`w-10 h-10 rounded-lg bg-gray-800 flex items-center justify-center ${stat.color}`}>
            <stat.icon className="w-5 h-5" />
          </div>
          <div>
            <p className="text-2xl font-bold text-white">{stat.value}</p>
            <p className="text-xs text-gray-400">{stat.label}</p>
          </div>
        </div>
      ))}
    </div>
  )
}

// =========================================================================
// MAIN COMPONENT: ThreatMap Page
// =========================================================================
export default function ThreatMap() {
  const [attacks, setAttacks] = useState([])
  const [loading, setLoading] = useState(true)
  const [lastRefresh, setLastRefresh] = useState(null)

  // Fetch attack geo data from API
  const fetchData = async () => {
    try {
      const data = await api.getAttackGeoData()
      setAttacks(data)
      setLastRefresh(new Date())
    } catch (error) {
      console.error('Error fetching geo attack data:', error)
    }
    setLoading(false)
  }

  // Initial fetch + auto-refresh every 15 seconds
  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, 15000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Threat Map</h1>
          <p className="text-gray-400 mt-1">
            Global visualization of attacker locations from honeypot data
          </p>
        </div>

        {/* Refresh Indicator */}
        <div className="flex items-center gap-2 text-sm text-gray-400">
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin text-cyan-400' : ''}`} />
          {lastRefresh && (
            <span>Updated {lastRefresh.toLocaleTimeString()}</span>
          )}
        </div>
      </div>

      {/* Summary Stats */}
      <StatsBar attacks={attacks} />

      {/* Map Container */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl overflow-hidden">
        {/* Map Header */}
        <div className="p-4 border-b border-cyan-500/20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Globe className="w-5 h-5 text-cyan-400" />
            <h3 className="text-lg font-semibold text-white">Live Attack Origins</h3>
          </div>

          {/* Legend */}
          <div className="flex items-center gap-4 text-xs">
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-red-500"></span>
              <span className="text-gray-400">High Risk</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-orange-500"></span>
              <span className="text-gray-400">Medium</span>
            </span>
            <span className="flex items-center gap-1">
              <span className="w-3 h-3 rounded-full bg-green-500"></span>
              <span className="text-gray-400">Low</span>
            </span>
          </div>
        </div>

        {/* Interactive Leaflet Map */}
        <div style={{ height: '500px', width: '100%' }}>
          <MapContainer
            center={MAP_CENTER}
            zoom={MAP_ZOOM}
            style={{ height: '100%', width: '100%', background: '#0a0a1a' }}
            scrollWheelZoom={true}
            zoomControl={true}
          >
            {/* Dark-themed map tiles from CARTO */}
            <TileLayer
              url={DARK_TILE_URL}
              attribution={TILE_ATTRIBUTION}
            />

            {/* Map refresh handler (accesses map instance) */}
            <MapRefreshHandler data={attacks} />

            {/* Plot red circle markers for each attacker */}
            {attacks.map((attack, index) => (
              <CircleMarker
                key={`${attack.ip}-${index}`}
                center={[attack.latitude, attack.longitude]}
                radius={getMarkerRadius(attack.commandCount)}
                pathOptions={{
                  color: getMarkerColor(attack.skillLevel),
                  fillColor: getMarkerColor(attack.skillLevel),
                  fillOpacity: 0.7,
                  weight: 2,
                  opacity: 0.9,
                }}
              >
                {/* Popup on click — shows attack details */}
                <Popup>
                  <div style={{
                    fontFamily: "'Inter', 'Segoe UI', sans-serif",
                    minWidth: '220px',
                    padding: '4px'
                  }}>
                    {/* IP Header */}
                    <div style={{
                      fontSize: '16px',
                      fontWeight: 'bold',
                      fontFamily: 'monospace',
                      color: '#e11d48',
                      marginBottom: '8px',
                      paddingBottom: '6px',
                      borderBottom: '1px solid #e5e7eb'
                    }}>
                      🎯 {attack.ip}
                    </div>

                    {/* Location Info */}
                    <div style={{ fontSize: '13px', lineHeight: '1.8' }}>
                      <div><strong>📍 Location:</strong> {attack.city}, {attack.country}</div>
                      <div><strong>🌐 Coordinates:</strong> {attack.latitude.toFixed(4)}, {attack.longitude.toFixed(4)}</div>
                      <div><strong>⚔️ Attack Type:</strong> {attack.attackType}</div>
                      <div><strong>📊 Commands:</strong> {attack.commandCount}</div>
                      <div><strong>📡 Sessions:</strong> {attack.sessionCount}</div>
                      <div>
                        <strong>⚠️ Skill Level: </strong>
                        <span style={{
                          color: attack.skillLevel === 'High' ? '#ef4444' :
                                 attack.skillLevel === 'Medium' ? '#f97316' : '#22c55e',
                          fontWeight: 'bold'
                        }}>
                          {attack.skillLevel}
                        </span>
                      </div>
                      <div style={{ fontSize: '11px', color: '#9ca3af', marginTop: '4px' }}>
                        🕐 {new Date(attack.timestamp).toLocaleString()}
                      </div>
                    </div>
                  </div>
                </Popup>
              </CircleMarker>
            ))}
          </MapContainer>
        </div>
      </div>

      {/* Attacker Table Below Map */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-cyan-500/20">
          <h3 className="text-lg font-semibold text-white">Attacker Locations</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-800">
                <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">IP Address</th>
                <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">Country</th>
                <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">City</th>
                <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">Commands</th>
                <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">Skill Level</th>
                <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">Attack Type</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800/50">
              {attacks.map((attack, index) => (
                <tr key={index} className="hover:bg-white/5 transition-colors">
                  <td className="py-3 px-4 text-white font-mono text-sm">{attack.ip}</td>
                  <td className="py-3 px-4 text-white">{attack.country}</td>
                  <td className="py-3 px-4 text-gray-300">{attack.city}</td>
                  <td className="py-3 px-4 text-white">{attack.commandCount}</td>
                  <td className="py-3 px-4">
                    <span className={`px-2 py-1 rounded text-xs font-medium ${
                      attack.skillLevel === 'High'   ? 'bg-red-500/20 text-red-400' :
                      attack.skillLevel === 'Medium' ? 'bg-orange-500/20 text-orange-400' :
                      'bg-green-500/20 text-green-400'
                    }`}>
                      {attack.skillLevel}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-gray-300 text-sm">{attack.attackType}</td>
                </tr>
              ))}
              {attacks.length === 0 && (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-gray-500">
                    {loading ? 'Loading attack data...' : 'No attacks recorded yet. Start the honeypot and connect via SSH to generate data.'}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
