import { NavLink, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  Terminal, 
  Play, 
  BarChart3, 
  Globe,
  Settings,
  Shield,
  Search,
  Bell,
  User
} from 'lucide-react'

const navItems = [
  { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
  { path: '/sessions', icon: Users, label: 'Live Sessions' },
  { path: '/timeline', icon: Terminal, label: 'Command Timeline' },
  { path: '/replay', icon: Play, label: 'Session Replay' },
  { path: '/analytics', icon: BarChart3, label: 'Analytics' },
  { path: '/threat-map', icon: Globe, label: 'Threat Map' },
  { path: '/settings', icon: Settings, label: 'Settings' },
]

function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-gray-900/80 backdrop-blur-xl border-r border-cyan-500/20 z-50">
      {/* Logo */}
      <div className="p-6 border-b border-cyan-500/20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center">
            <Shield className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Honeypot AI</h1>
            <p className="text-xs text-cyan-400">Threat Intelligence</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300 ${
                isActive
                  ? 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-400 border border-cyan-500/30'
                  : 'text-gray-400 hover:text-white hover:bg-white/5'
              }`
            }
          >
            <item.icon className="w-5 h-5" />
            <span className="font-medium">{item.label}</span>
          </NavLink>
        ))}
      </nav>

      {/* System Status */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-cyan-500/20">
        <div className="flex items-center gap-2 text-sm">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-green-400">System Active</span>
        </div>
        <p className="text-xs text-gray-500 mt-1">Honeypot running on port 2222</p>
      </div>
    </aside>
  )
}

function TopBar() {
  const location = useLocation()
  
  const getPageTitle = () => {
    const titles = {
      '/': 'Dashboard',
      '/sessions': 'Live Sessions',
      '/timeline': 'Command Timeline',
      '/replay': 'Session Replay',
      '/analytics': 'Analytics',
      '/threat-map': 'Threat Map',
      '/settings': 'Settings'
    }
    return titles[location.pathname] || 'Dashboard'
  }

  return (
    <header className="h-16 bg-gray-900/60 backdrop-blur-xl border-b border-cyan-500/20 flex items-center justify-between px-6">
      <h2 className="text-xl font-semibold text-white">{getPageTitle()}</h2>
      
      <div className="flex items-center gap-6">
        {/* Search */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            placeholder="Search IP, command..."
            className="pl-10 pr-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-sm text-white placeholder-gray-500 focus:outline-none focus:border-cyan-500 transition-colors w-64"
          />
        </div>

        {/* Status */}
        <div className="flex items-center gap-2 px-3 py-1.5 bg-green-500/10 border border-green-500/30 rounded-full">
          <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-sm text-green-400">System Active</span>
        </div>

        {/* Notifications */}
        <button className="relative p-2 text-gray-400 hover:text-white transition-colors">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-red-500"></span>
        </button>

        {/* Profile */}
        <button className="w-9 h-9 rounded-full bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center">
          <User className="w-5 h-5 text-white" />
        </button>
      </div>
    </header>
  )
}

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-gray-950">
      {/* Background Effects */}
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-cyan-900/20 via-gray-950 to-gray-950 pointer-events-none"></div>
      <div className="fixed inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMwLTkuOTQtOC4wNi0xOC0xOC0xOFMwIDguMDYgMCAxOHM4LjA2IDE4IDE4IDE4IDE4LTguMDYgMTgtMTgiIHN0cm9rZT0iIzBmYjRlMzEwIi8+PC9nPjwvc3ZnPg==')] opacity-30 pointer-events-none"></div>
      
      <Sidebar />
      
      <div className="ml-64">
        <TopBar />
        <main className="p-6 relative">
          {children}
        </main>
      </div>
    </div>
  )
}
