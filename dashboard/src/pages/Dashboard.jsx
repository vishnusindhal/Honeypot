import { useState, useEffect } from 'react'
import { Users, Terminal, AlertTriangle, Clock, RefreshCw } from 'lucide-react'
import MetricCard from '../components/MetricCard'
import SessionsTable from '../components/SessionsTable'
import CommandFeed from '../components/CommandFeed'
import { CommandBarChart, RiskDonutChart, TimelineChart } from '../components/Charts'
import api from '../services/api'

export default function Dashboard() {
  const [metrics, setMetrics] = useState({
    activeSessions: 0,
    totalCommands: 0,
    highRiskActions: 0,
    avgSessionDuration: "0m 0s"
  })
  const [sessions, setSessions] = useState([])
  const [commands, setCommands] = useState([])
  const [commandFrequency, setCommandFrequency] = useState([])
  const [riskDistribution, setRiskDistribution] = useState([])
  const [timelineData, setTimelineData] = useState([])
  const [loading, setLoading] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(null)

  const fetchData = async () => {
    setLoading(true)
    try {
      const [metricsData, sessionsData, commandsData, freqData, riskData, timelineDataRes] = await Promise.all([
        api.getMetrics(),
        api.getSessions(),
        api.getCommands(),
        api.getCommandFrequency(),
        api.getRiskDistribution(),
        api.getTimeline()
      ])
      
      setMetrics(metricsData)
      setSessions(sessionsData)
      setCommands(commandsData)
      setCommandFrequency(freqData)
      setRiskDistribution(riskData)
      setTimelineData(timelineDataRes)
      setLastUpdate(new Date())
    } catch (error) {
      console.error('Error fetching data:', error)
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchData()
    
    // Auto-refresh every 10 seconds
    const interval = setInterval(fetchData, 10000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="space-y-6">
      {/* Header with refresh */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className={`w-3 h-3 rounded-full ${loading ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`}></div>
          <span className="text-sm text-gray-400">
            {lastUpdate ? `Last updated: ${lastUpdate.toLocaleTimeString()}` : 'Loading...'}
          </span>
        </div>
        <button 
          onClick={fetchData}
          disabled={loading}
          className="flex items-center gap-2 px-3 py-1.5 bg-cyan-500/20 text-cyan-400 rounded-lg hover:bg-cyan-500/30 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Active Sessions"
          value={metrics.activeSessions}
          change={metrics.activeSessions > 0 ? `+${metrics.activeSessions}` : '0'}
          changeType={metrics.activeSessions > 0 ? 'negative' : 'positive'}
          icon={Users}
        />
        <MetricCard
          title="Total Commands"
          value={metrics.totalCommands}
          change={`${metrics.totalCommands}`}
          changeType="negative"
          icon={Terminal}
        />
        <MetricCard
          title="High-Risk Actions"
          value={metrics.highRiskActions}
          change={metrics.highRiskActions > 0 ? `${metrics.highRiskActions} detected` : '0'}
          changeType={metrics.highRiskActions > 0 ? 'negative' : 'positive'}
          icon={AlertTriangle}
        />
        <MetricCard
          title="Avg Session Duration"
          value={metrics.avgSessionDuration}
          icon={Clock}
        />
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sessions Table - 2 columns */}
        <div className="lg:col-span-2">
          <SessionsTable sessions={sessions} />
        </div>
        
        {/* Command Feed - 1 column */}
        <div>
          <CommandFeed commands={commands} />
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <CommandBarChart data={commandFrequency} />
        <RiskDonutChart data={riskDistribution} />
        <TimelineChart data={timelineData} />
      </div>
    </div>
  )
}
