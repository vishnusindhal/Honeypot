import { useState, useEffect } from 'react'
import TerminalReplay from '../components/TerminalReplay'
import api from '../services/api'

export default function SessionReplay() {
  const [sessions, setSessions] = useState([])
  const [selectedSession, setSelectedSession] = useState(null)
  const [replayData, setReplayData] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchSessions = async () => {
      setLoading(true)
      try {
        const data = await api.getSessions()
        setSessions(data)
        if (data.length > 0 && !selectedSession) {
          setSelectedSession(data[0])
        }
      } catch (error) {
        console.error('Error fetching sessions:', error)
      }
      setLoading(false)
    }
    
    fetchSessions()
  }, [])

  useEffect(() => {
    const fetchReplayData = async () => {
      if (selectedSession?.id) {
        try {
          const data = await api.getSessionReplay(selectedSession.id)
          setReplayData(data)
        } catch (error) {
          console.error('Error fetching replay data:', error)
        }
      }
    }
    
    fetchReplayData()
  }, [selectedSession])

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Session Replay</h1>
          <p className="text-gray-400 mt-1">Replay recorded attacker sessions step-by-step</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Session List */}
        <div className="lg:col-span-1">
          <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl overflow-hidden">
            <div className="p-4 border-b border-cyan-500/20">
              <h3 className="text-lg font-semibold text-white">Sessions ({sessions.length})</h3>
            </div>
            {loading ? (
              <div className="p-4 text-gray-400">Loading...</div>
            ) : (
              <div className="divide-y divide-gray-800 max-h-96 overflow-y-auto">
                {sessions.map((session) => (
                  <button
                    key={session.id}
                    onClick={() => setSelectedSession(session)}
                    className={`w-full p-4 text-left hover:bg-white/5 transition-colors ${
                      selectedSession?.id === session.id ? 'bg-cyan-500/10 border-l-2 border-cyan-500' : ''
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`w-2 h-2 rounded-full ${session.status === 'Active' ? 'bg-green-500' : 'bg-gray-500'}`}></span>
                      <span className="text-white font-mono text-sm">{session.ip}</span>
                    </div>
                    <p className="text-xs text-gray-500">{session.commandCount} commands</p>
                    <p className="text-xs text-gray-600 mt-1">User: {session.username}</p>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Terminal Replay */}
        <div className="lg:col-span-3">
          <TerminalReplay replayData={replayData} />
          
          {/* Session Info */}
          {selectedSession && (
            <div className="mt-6 bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Session Details</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-xs text-gray-500 mb-1">Attacker IP</p>
                  <p className="text-white font-mono">{selectedSession.ip}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Username</p>
                  <p className="text-white">{selectedSession.username}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Skill Level</p>
                  <p className={`${
                    selectedSession.skillLevel === 'High' ? 'text-red-400' :
                    selectedSession.skillLevel === 'Medium' ? 'text-orange-400' : 'text-green-400'
                  }`}>{selectedSession.skillLevel}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 mb-1">Commands</p>
                  <p className="text-white">{selectedSession.commandCount}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
