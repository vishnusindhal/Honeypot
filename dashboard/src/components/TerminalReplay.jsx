import { useState, useEffect, useRef } from 'react'
import { Play, Pause, SkipForward, RotateCcw, Download } from 'lucide-react'

export default function TerminalReplay({ replayData }) {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentIndex, setCurrentIndex] = useState(0)
  const [displayedCommands, setDisplayedCommands] = useState([])
  const terminalRef = useRef(null)
  const intervalRef = useRef(null)

  useEffect(() => {
    if (isPlaying && currentIndex < replayData.length) {
      const currentCommand = replayData[currentIndex]
      const delay = currentIndex === 0 ? 500 : replayData[currentIndex].timestamp - replayData[currentIndex - 1].timestamp
      
      intervalRef.current = setTimeout(() => {
        setDisplayedCommands(prev => [...prev, currentCommand])
        setCurrentIndex(prev => prev + 1)
        
        // Auto-scroll
        if (terminalRef.current) {
          terminalRef.current.scrollTop = terminalRef.current.scrollHeight
        }
      }, Math.min(delay, 2000)) // Cap delay at 2 seconds
    } else if (currentIndex >= replayData.length) {
      setIsPlaying(false)
    }
    
    return () => clearTimeout(intervalRef.current)
  }, [isPlaying, currentIndex, replayData])

  const handlePlay = () => setIsPlaying(true)
  const handlePause = () => setIsPlaying(false)
  
  const handleStep = () => {
    if (currentIndex < replayData.length) {
      setDisplayedCommands(prev => [...prev, replayData[currentIndex]])
      setCurrentIndex(prev => prev + 1)
    }
  }
  
  const handleReset = () => {
    setIsPlaying(false)
    setCurrentIndex(0)
    setDisplayedCommands([])
  }

  const progress = replayData.length > 0 ? (currentIndex / replayData.length) * 100 : 0

  return (
    <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl overflow-hidden">
      {/* Terminal Header */}
      <div className="bg-gray-800 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 rounded-full bg-red-500"></span>
          <span className="w-3 h-3 rounded-full bg-yellow-500"></span>
          <span className="w-3 h-3 rounded-full bg-green-500"></span>
          <span className="ml-4 text-gray-400 text-sm font-mono">admin@prod-db-01</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">
            {currentIndex}/{replayData.length} commands
          </span>
        </div>
      </div>

      {/* Terminal Body */}
      <div 
        ref={terminalRef}
        className="bg-gray-950 p-4 font-mono text-sm h-96 overflow-y-auto"
      >
        <div className="text-green-400 mb-4">
          Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-150-generic x86_64)
        </div>
        
        {displayedCommands.map((cmd, index) => (
          <div key={index} className="mb-3 animate-fadeIn">
            <div className="flex items-center gap-2">
              <span className="text-cyan-400">admin@prod-db-01</span>
              <span className="text-gray-500">:</span>
              <span className="text-blue-400">~</span>
              <span className="text-gray-500">$</span>
              <span className="text-white typing-animation">{cmd.command}</span>
            </div>
            {cmd.output && (
              <div className="text-gray-400 mt-1 pl-4 whitespace-pre-wrap">
                {cmd.output}
              </div>
            )}
          </div>
        ))}
        
        {isPlaying && currentIndex < replayData.length && (
          <div className="flex items-center gap-2">
            <span className="text-cyan-400">admin@prod-db-01</span>
            <span className="text-gray-500">:</span>
            <span className="text-blue-400">~</span>
            <span className="text-gray-500">$</span>
            <span className="animate-pulse">▋</span>
          </div>
        )}
      </div>

      {/* Progress Bar */}
      <div className="h-1 bg-gray-800">
        <div 
          className="h-full bg-gradient-to-r from-cyan-500 to-purple-500 transition-all duration-300"
          style={{ width: `${progress}%` }}
        ></div>
      </div>

      {/* Controls */}
      <div className="bg-gray-800/50 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          {isPlaying ? (
            <button 
              onClick={handlePause}
              className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg hover:bg-cyan-500/30 transition-colors"
            >
              <Pause className="w-5 h-5" />
            </button>
          ) : (
            <button 
              onClick={handlePlay}
              className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg hover:bg-cyan-500/30 transition-colors"
            >
              <Play className="w-5 h-5" />
            </button>
          )}
          <button 
            onClick={handleStep}
            className="p-2 bg-gray-700/50 text-gray-400 rounded-lg hover:bg-gray-700 hover:text-white transition-colors"
          >
            <SkipForward className="w-5 h-5" />
          </button>
          <button 
            onClick={handleReset}
            className="p-2 bg-gray-700/50 text-gray-400 rounded-lg hover:bg-gray-700 hover:text-white transition-colors"
          >
            <RotateCcw className="w-5 h-5" />
          </button>
        </div>
        
        <button className="flex items-center gap-2 px-3 py-1.5 bg-gray-700/50 text-gray-400 rounded-lg hover:bg-gray-700 hover:text-white transition-colors">
          <Download className="w-4 h-4" />
          <span className="text-sm">Export</span>
        </button>
      </div>
    </div>
  )
}
