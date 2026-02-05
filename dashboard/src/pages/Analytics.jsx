import { useState, useEffect } from 'react'
import { CommandBarChart, RiskDonutChart, TimelineChart, SkillHeatmap } from '../components/Charts'
import api from '../services/api'

export default function Analytics() {
  const [metrics, setMetrics] = useState({ totalCommands: 0 })
  const [commandFrequency, setCommandFrequency] = useState([])
  const [riskDistribution, setRiskDistribution] = useState([])
  const [skillDistribution, setSkillDistribution] = useState([])
  const [timelineData, setTimelineData] = useState([])
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const [metricsData, freqData, riskData, skillData, timeData, sessionsData] = await Promise.all([
          api.getMetrics(),
          api.getCommandFrequency(),
          api.getRiskDistribution(),
          api.getSkillDistribution(),
          api.getTimeline(),
          api.getSessions()
        ])
        
        setMetrics(metricsData)
        setCommandFrequency(freqData)
        setRiskDistribution(riskData)
        setSkillDistribution(skillData)
        setTimelineData(timeData)
        setSessions(sessionsData)
      } catch (error) {
        console.error('Error fetching analytics:', error)
      }
      setLoading(false)
    }
    
    fetchData()
    const interval = setInterval(fetchData, 30000) // Refresh every 30 seconds
    return () => clearInterval(interval)
  }, [])

  // Count sessions by country
  const countryStats = sessions.reduce((acc, session) => {
    const country = session.country || 'Unknown'
    acc[country] = (acc[country] || 0) + 1
    return acc
  }, {})

  const uniqueIPs = new Set(sessions.map(s => s.ip)).size

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Analytics</h1>
        <p className="text-gray-400 mt-1">Comprehensive threat intelligence insights from live data</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-6">
          <p className="text-gray-400 text-sm">Total Sessions</p>
          <p className="text-3xl font-bold text-white mt-2">{sessions.length}</p>
          <p className="text-cyan-400 text-sm mt-1">From honeypot logs</p>
        </div>
        <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-6">
          <p className="text-gray-400 text-sm">Unique IPs</p>
          <p className="text-3xl font-bold text-white mt-2">{uniqueIPs}</p>
          <p className="text-cyan-400 text-sm mt-1">Distinct attackers</p>
        </div>
        <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-6">
          <p className="text-gray-400 text-sm">High-Skill Attackers</p>
          <p className="text-3xl font-bold text-red-400 mt-2">
            {sessions.filter(s => s.skillLevel === 'High').length}
          </p>
          <p className="text-red-400 text-sm mt-1">Requires attention</p>
        </div>
        <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-6">
          <p className="text-gray-400 text-sm">Commands Captured</p>
          <p className="text-3xl font-bold text-white mt-2">{metrics.totalCommands}</p>
          <p className="text-purple-400 text-sm mt-1">Total logged</p>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CommandBarChart data={commandFrequency} />
        <RiskDonutChart data={riskDistribution} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TimelineChart data={timelineData} />
        <SkillHeatmap data={skillDistribution} />
      </div>

      {/* Top Sessions Table */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-cyan-500/20">
          <h3 className="text-lg font-semibold text-white">Session Summary</h3>
        </div>
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-800">
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">IP Address</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">Username</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">Commands</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase">Skill Level</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/50">
            {sessions.slice(0, 5).map((session, index) => (
              <tr key={index} className="hover:bg-white/5">
                <td className="py-3 px-4 text-white font-mono">{session.ip}</td>
                <td className="py-3 px-4 text-white">{session.username}</td>
                <td className="py-3 px-4 text-white">{session.commandCount}</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded text-xs ${
                    session.skillLevel === 'High' ? 'bg-red-500/20 text-red-400' :
                    session.skillLevel === 'Medium' ? 'bg-orange-500/20 text-orange-400' :
                    'bg-green-500/20 text-green-400'
                  }`}>{session.skillLevel}</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
