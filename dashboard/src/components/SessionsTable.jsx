import { Eye, MoreVertical } from 'lucide-react'

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

const statusColors = {
  Active: 'text-green-400',
  Ended: 'text-gray-500'
}

export default function SessionsTable({ sessions }) {
  return (
    <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl overflow-hidden">
      <div className="p-4 border-b border-cyan-500/20 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Live Sessions</h3>
        <button className="text-cyan-400 text-sm hover:text-cyan-300 transition-colors">
          View All →
        </button>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-800">
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Session ID</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Attacker IP</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Country</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Skill Level</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Risk</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Commands</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
              <th className="text-left py-3 px-4 text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800/50">
            {sessions.map((session) => (
              <tr key={session.id} className="hover:bg-white/5 transition-colors">
                <td className="py-3 px-4">
                  <span className="text-cyan-400 font-mono text-sm">{session.id.slice(0, 16)}...</span>
                </td>
                <td className="py-3 px-4">
                  <span className="text-white font-mono">{session.ip}</span>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    <span className="text-lg">{getFlagEmoji(session.countryCode)}</span>
                    <span className="text-gray-300">{session.country}</span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${skillColors[session.skillLevel]}`}>
                    {session.skillLevel}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-medium border ${riskColors[session.riskLevel]}`}>
                    {session.riskLevel}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <span className="text-white">{session.commandCount}</span>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    <span className={`w-2 h-2 rounded-full ${session.status === 'Active' ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`}></span>
                    <span className={statusColors[session.status]}>{session.status}</span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    <button className="p-1.5 text-gray-400 hover:text-cyan-400 hover:bg-cyan-500/10 rounded-lg transition-colors">
                      <Eye className="w-4 h-4" />
                    </button>
                    <button className="p-1.5 text-gray-400 hover:text-white hover:bg-white/10 rounded-lg transition-colors">
                      <MoreVertical className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

function getFlagEmoji(countryCode) {
  const flags = {
    RU: '🇷🇺',
    CN: '🇨🇳',
    VN: '🇻🇳',
    DE: '🇩🇪',
    US: '🇺🇸',
    KP: '🇰🇵',
    IR: '🇮🇷',
    BR: '🇧🇷'
  }
  return flags[countryCode] || '🌍'
}
