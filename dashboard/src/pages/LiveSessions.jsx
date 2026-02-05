import { useState, useEffect } from 'react'
import { Search, Filter, Download, Eye, Play, Trash2, RefreshCw } from 'lucide-react'
import api from '../services/api'

const skillColors = {
  High: 'bg-red-500/20 text-red-400 border-red-500/30',
  Medium: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  Low: 'bg-green-500/20 text-green-400 border-green-500/30'
}

const riskColors = {
  Critical: 'bg-red-500/20 text-red-400 border-red-500/30',
  High: 'bg-orange-500/20 text-orange-400 border-orange-500/30',
  Medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  Low: 'bg-green-500/20 text-green-400 border-green-500/30'
}

const getFlagEmoji = (countryCode) => {
  const flags = { RU: '🇷🇺', CN: '🇨🇳', VN: '🇻🇳', DE: '🇩🇪', US: '🇺🇸', UN: '🌍' }
  return flags[countryCode] || '🌍'
}

export default function LiveSessions() {
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStatus, setFilterStatus] = useState('all')
  
  const fetchSessions = async () => {
    setLoading(true)
    try {
      const data = await api.getSessions()
      setSessions(data)
    } catch (error) {
      console.error('Error fetching sessions:', error)
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchSessions()
    const interval = setInterval(fetchSessions, 10000)
    return () => clearInterval(interval)
  }, [])
  
  const filteredSessions = sessions.filter(session => {
    const matchesSearch = session.ip?.includes(searchTerm) || 
                          session.id?.includes(searchTerm) ||
                          session.username?.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesFilter = filterStatus === 'all' || session.status?.toLowerCase() === filterStatus
    return matchesSearch && matchesFilter
  })

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Live Sessions</h1>
          <p className="text-gray-400 mt-1">Monitor active attacker connections in real-time</p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={fetchSessions}
            disabled={loading}
            className="flex items-center gap-2 px-3 py-2 bg-gray-700/50 text-gray-400 rounded-lg hover:bg-gray-700 hover:text-white transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-lg hover:bg-cyan-500/30 transition-colors">
            <Download className="w-4 h-4" />
            Export All
          </button>
        </div>
      </div>

      {/* Filters Bar */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-4">
        <div className="flex flex-wrap items-center gap-4">
          <div className="relative flex-1 min-w-64">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
            <input
              type="text"
              placeholder="Search by IP, session ID, username..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors"
            />
          </div>
          
          <div className="flex items-center gap-2">
            <Filter className="w-4 h-4 text-gray-500" />
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
              className="px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
            >
              <option value="all">All Status</option>
              <option value="active">Active Only</option>
              <option value="ended">Ended Only</option>
            </select>
          </div>
          
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            {filteredSessions.length} sessions
          </div>
        </div>
      </div>

      {/* Sessions Grid */}
      {loading && sessions.length === 0 ? (
        <div className="text-center py-12 text-gray-400">Loading sessions...</div>
      ) : filteredSessions.length === 0 ? (
        <div className="text-center py-12 text-gray-400">No sessions found</div>
      ) : (
        <div className="grid gap-4">
          {filteredSessions.map((session) => (
            <div 
              key={session.id}
              className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-6 hover:border-cyan-500/40 transition-all duration-300"
            >
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                  {/* Status Indicator */}
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                    session.status === 'Active' 
                      ? 'bg-green-500/20 border border-green-500/30' 
                      : 'bg-gray-700/50 border border-gray-600'
                  }`}>
                    <span className="text-2xl">{getFlagEmoji(session.countryCode)}</span>
                  </div>
                  
                  <div>
                    <div className="flex items-center gap-3">
                      <h3 className="text-lg font-semibold text-white font-mono">{session.ip}</h3>
                      <span className={`w-2 h-2 rounded-full ${session.status === 'Active' ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`}></span>
                      <span className={`text-sm ${session.status === 'Active' ? 'text-green-400' : 'text-gray-500'}`}>
                        {session.status}
                      </span>
                    </div>
                    <p className="text-gray-400 text-sm mt-1">
                      Session: <span className="text-cyan-400 font-mono">{session.id}</span>
                    </p>
                    <div className="flex items-center gap-4 mt-3">
                      <div className="flex items-center gap-2">
                        <span className="text-gray-500 text-sm">User:</span>
                        <span className="text-white">{session.username}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-gray-500 text-sm">Commands:</span>
                        <span className="text-white">{session.commandCount}</span>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-start gap-6">
                  {/* Badges */}
                  <div className="flex flex-col items-end gap-2">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${skillColors[session.skillLevel] || skillColors.Low}`}>
                      Skill: {session.skillLevel}
                    </span>
                    <span className={`px-3 py-1 rounded-full text-xs font-medium border ${riskColors[session.riskLevel] || riskColors.Low}`}>
                      Risk: {session.riskLevel}
                    </span>
                  </div>
                  
                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <button className="p-2 text-gray-400 hover:text-cyan-400 hover:bg-cyan-500/10 rounded-lg transition-colors">
                      <Eye className="w-5 h-5" />
                    </button>
                    <button className="p-2 text-gray-400 hover:text-green-400 hover:bg-green-500/10 rounded-lg transition-colors">
                      <Play className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
              
              {/* Last Command */}
              {session.lastCommand && (
                <div className="mt-4 pt-4 border-t border-gray-800">
                  <p className="text-xs text-gray-500 mb-1">Last Command:</p>
                  <div className="bg-gray-950/50 rounded-lg p-3 font-mono text-sm">
                    <span className="text-green-400">$ </span>
                    <span className="text-white">{session.lastCommand}</span>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
