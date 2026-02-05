const categoryColors = {
  'Recon': 'border-cyan-500 bg-cyan-500/10',
  'Reconnaissance': 'border-cyan-500 bg-cyan-500/10',
  'Privilege Escalation': 'border-orange-500 bg-orange-500/10',
  'PrivEsc': 'border-orange-500 bg-orange-500/10',
  'Persistence': 'border-red-500 bg-red-500/10',
  'Credential Harvesting': 'border-purple-500 bg-purple-500/10',
  'Exfiltration': 'border-yellow-500 bg-yellow-500/10',
  'Anti-Forensics': 'border-pink-500 bg-pink-500/10'
}

const categoryTextColors = {
  'Recon': 'text-cyan-400',
  'Reconnaissance': 'text-cyan-400',
  'Privilege Escalation': 'text-orange-400',
  'PrivEsc': 'text-orange-400',
  'Persistence': 'text-red-400',
  'Credential Harvesting': 'text-purple-400',
  'Exfiltration': 'text-yellow-400',
  'Anti-Forensics': 'text-pink-400'
}

export default function CommandFeed({ commands, maxItems = 8 }) {
  const displayCommands = commands.slice(0, maxItems)
  
  return (
    <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl overflow-hidden">
      <div className="p-4 border-b border-cyan-500/20 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-white">Command Timeline</h3>
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-sm text-gray-400">Live</span>
        </div>
      </div>
      
      <div className="divide-y divide-gray-800/50 max-h-96 overflow-y-auto">
        {displayCommands.map((cmd, index) => (
          <div 
            key={cmd.id} 
            className={`p-4 hover:bg-white/5 transition-all duration-300 border-l-2 ${categoryColors[cmd.category] || 'border-gray-500 bg-gray-500/10'}`}
            style={{ animationDelay: `${index * 100}ms` }}
          >
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-2">
                <span className={`text-xs font-medium ${categoryTextColors[cmd.category] || 'text-gray-400'}`}>
                  {cmd.category}
                </span>
                <span className="text-xs text-gray-600">•</span>
                <span className="text-xs text-gray-500 font-mono">
                  {new Date(cmd.timestamp).toLocaleTimeString()}
                </span>
              </div>
              <span className="text-xs text-gray-600 font-mono">{cmd.sessionId.slice(8, 20)}</span>
            </div>
            
            <div className="bg-gray-950/50 rounded-lg p-3 font-mono">
              <div className="flex items-center gap-2 text-sm">
                <span className="text-green-400">$</span>
                <span className="text-white">{cmd.command}</span>
              </div>
              {cmd.output && (
                <div className="mt-2 text-xs text-gray-500 border-t border-gray-800 pt-2">
                  {cmd.output.slice(0, 100)}{cmd.output.length > 100 ? '...' : ''}
                </div>
              )}
            </div>
            
            <div className="mt-2 flex items-center gap-2">
              <span className="text-xs text-gray-500">Intent:</span>
              <span className={`text-xs ${categoryTextColors[cmd.category] || 'text-gray-400'}`}>
                {cmd.intent}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
