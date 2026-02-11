import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import LiveSessions from './pages/LiveSessions'
import CommandTimeline from './pages/CommandTimeline'
import SessionReplay from './pages/SessionReplay'
import Analytics from './pages/Analytics'
import ThreatMap from './pages/ThreatMap'
import Settings from './pages/Settings'
import './index.css'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/sessions" element={<LiveSessions />} />
          <Route path="/timeline" element={<CommandTimeline />} />
          <Route path="/replay" element={<SessionReplay />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/threat-map" element={<ThreatMap />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
