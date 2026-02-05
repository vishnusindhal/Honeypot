import { useState, useEffect } from 'react'
import { Filter, Download, ChevronDown, ChevronRight, RefreshCw } from 'lucide-react'
import api from '../services/api'

const categoryColors = {
  'Recon': { bg: 'bg-cyan-500/20', border: 'border-cyan-500', text: 'text-cyan-400' },
  'Reconnaissance': { bg: 'bg-cyan-500/20', border: 'border-cyan-500', text: 'text-cyan-400' },
  'Privilege Escalation': { bg: 'bg-orange-500/20', border: 'border-orange-500', text: 'text-orange-400' },
  'Persistence': { bg: 'bg-red-500/20', border: 'border-red-500', text: 'text-red-400' },
  'Credential Harvesting': { bg: 'bg-purple-500/20', border: 'border-purple-500', text: 'text-purple-400' },
  'Exfiltration': { bg: 'bg-yellow-500/20', border: 'border-yellow-500', text: 'text-yellow-400' },
  'Exfiltration/Network': { bg: 'bg-yellow-500/20', border: 'border-yellow-500', text: 'text-yellow-400' },
  'Anti-Forensics': { bg: 'bg-pink-500/20', border: 'border-pink-500', text: 'text-pink-400' },
  'Command Execution': { bg: 'bg-gray-500/20', border: 'border-gray-500', text: 'text-gray-400' },
  'Unknown': { bg: 'bg-gray-500/20', border: 'border-gray-500', text: 'text-gray-400' }
}

export default function CommandTimeline() {
  const [commands, setCommands] = useState([])
  const [loading, setLoading] = useState(true)
  const [expandedItems, setExpandedItems] = useState(new Set())
  const [filterCategory, setFilterCategory] = useState('all')
  
  const fetchCommands = async () => {
    setLoading(true)
    try {
      const data = await api.getCommands()
      setCommands(data)
    } catch (error) {
      console.error('Error fetching commands:', error)
    }
    setLoading(false)
  }

  useEffect(() => {
    fetchCommands()
    const interval = setInterval(fetchCommands, 10000)
    return () => clearInterval(interval)
  }, [])
  
  const toggleExpand = (id) => {
    const newExpanded = new Set(expandedItems)
    if (newExpanded.has(id)) {
      newExpanded.delete(id)
    } else {
      newExpanded.add(id)
    }
    setExpandedItems(newExpanded)
  }

  const categories = ['all', ...new Set(commands.map(c => c.category))]
  
  const filteredLogs = filterCategory === 'all' 
    ? commands 
    : commands.filter(c => c.category === filterCategory)

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Command Timeline</h1>
          <p className="text-gray-400 mt-1">Real-time feed of all executed commands</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/30 rounded-full">
            <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
            <span className="text-sm text-green-400">Live</span>
          </div>
          <button 
            onClick={fetchCommands}
            disabled={loading}
            className="p-2 bg-gray-700/50 text-gray-400 rounded-lg hover:bg-gray-700 hover:text-white transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-lg hover:bg-cyan-500/30 transition-colors">
            <Download className="w-4 h-4" />
            Export
          </button>
        </div>
      </div>

      {/* Category Filter */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-4">
        <div className="flex items-center gap-2 overflow-x-auto pb-2">
          <Filter className="w-4 h-4 text-gray-500 shrink-0" />
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterCategory(cat)}
              className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                filterCategory === cat
                  ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`}
            >
              {cat === 'all' ? 'All Categories' : cat}
            </button>
          ))}
        </div>
      </div>

      {/* Timeline */}
      {loading && commands.length === 0 ? (
        <div className="text-center py-12 text-gray-400">Loading commands...</div>
      ) : filteredLogs.length === 0 ? (
        <div className="text-center py-12 text-gray-400">No commands found</div>
      ) : (
        <div className="relative">
          {/* Timeline Line */}
          <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-gradient-to-b from-cyan-500 via-purple-500 to-pink-500"></div>
          
          <div className="space-y-4">
            {filteredLogs.map((cmd, index) => {
              const colors = categoryColors[cmd.category] || categoryColors['Unknown']
              const isExpanded = expandedItems.has(cmd.id)
              
              return (
                <div key={cmd.id} className="relative pl-16">
                  {/* Timeline Dot */}
                  <div className={`absolute left-4 top-6 w-5 h-5 rounded-full ${colors.bg} ${colors.border} border-2 z-10`}></div>
                  
                  {/* Card */}
                  <div 
                    className={`bg-gray-900/60 backdrop-blur-xl border ${colors.border}/30 rounded-xl overflow-hidden hover:border-opacity-60 transition-all duration-300`}
                  >
                    <div 
                      className="p-4 cursor-pointer"
                      onClick={() => toggleExpand(cmd.id)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-2">
                            <span className={`px-2 py-0.5 rounded text-xs font-medium ${colors.bg} ${colors.text}`}>
                              {cmd.category}
                            </span>
                            <span className="text-xs text-gray-500 font-mono">
                              {cmd.timestamp ? new Date(cmd.timestamp).toLocaleString() : 'N/A'}
                            </span>
                            <span className="text-xs text-gray-600">•</span>
                            <span className="text-xs text-gray-500 font-mono">
                              {cmd.sessionId?.slice(0, 20) || 'unknown'}...
                            </span>
                          </div>
                          
                          <div className="bg-gray-950/50 rounded-lg p-3 font-mono">
                            <span className="text-green-400">$ </span>
                            <span className="text-white">{cmd.command}</span>
                          </div>
                        </div>
                        
                        <button className="ml-4 p-2 text-gray-500 hover:text-white transition-colors">
                          {isExpanded ? <ChevronDown className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
                        </button>
                      </div>
                    </div>
                    
                    {/* Expanded Content */}
                    {isExpanded && (
                      <div className="px-4 pb-4 border-t border-gray-800 pt-4">
                        <div className="grid grid-cols-2 gap-4 mb-4">
                          <div>
                            <p className="text-xs text-gray-500 mb-1">Intent</p>
                            <p className={`text-sm ${colors.text}`}>{cmd.intent}</p>
                          </div>
                          <div>
                            <p className="text-xs text-gray-500 mb-1">Skill Level</p>
                            <p className="text-sm text-white">{cmd.skillLevel}</p>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
