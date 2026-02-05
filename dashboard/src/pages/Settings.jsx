import { useState } from 'react'
import { Save, Shield, Bell, Database, Globe, Key } from 'lucide-react'

export default function Settings() {
  const [settings, setSettings] = useState({
    honeypotPort: 2222,
    maxSessions: 100,
    logRetention: 30,
    enableAlerts: true,
    alertEmail: 'security@company.com',
    slackWebhook: '',
    geoBlocking: false,
    blockedCountries: []
  })

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-white">Settings</h1>
        <p className="text-gray-400 mt-1">Configure your honeypot system</p>
      </div>

      {/* Honeypot Configuration */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-cyan-500/20 flex items-center gap-3">
          <Shield className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-semibold text-white">Honeypot Configuration</h3>
        </div>
        <div className="p-6 space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">SSH Port</label>
              <input
                type="number"
                value={settings.honeypotPort}
                onChange={(e) => setSettings({...settings, honeypotPort: e.target.value})}
                className="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
              />
              <p className="text-xs text-gray-500 mt-1">Port for SSH honeypot (default: 2222)</p>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-400 mb-2">Max Concurrent Sessions</label>
              <input
                type="number"
                value={settings.maxSessions}
                onChange={(e) => setSettings({...settings, maxSessions: e.target.value})}
                className="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-400 mb-2">Log Retention (days)</label>
            <input
              type="number"
              value={settings.logRetention}
              onChange={(e) => setSettings({...settings, logRetention: e.target.value})}
              className="w-full max-w-xs px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
            />
          </div>
        </div>
      </div>

      {/* Alert Configuration */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-cyan-500/20 flex items-center gap-3">
          <Bell className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-semibold text-white">Alert Settings</h3>
        </div>
        <div className="p-6 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white font-medium">Enable Alerts</p>
              <p className="text-sm text-gray-500">Receive notifications for high-risk activities</p>
            </div>
            <button
              onClick={() => setSettings({...settings, enableAlerts: !settings.enableAlerts})}
              className={`w-14 h-8 rounded-full transition-colors ${settings.enableAlerts ? 'bg-cyan-500' : 'bg-gray-700'}`}
            >
              <span className={`block w-6 h-6 bg-white rounded-full shadow transform transition-transform ${settings.enableAlerts ? 'translate-x-7' : 'translate-x-1'}`}></span>
            </button>
          </div>
          
          {settings.enableAlerts && (
            <>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Alert Email</label>
                <input
                  type="email"
                  value={settings.alertEmail}
                  onChange={(e) => setSettings({...settings, alertEmail: e.target.value})}
                  className="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white focus:outline-none focus:border-cyan-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-400 mb-2">Slack Webhook URL</label>
                <input
                  type="text"
                  value={settings.slackWebhook}
                  onChange={(e) => setSettings({...settings, slackWebhook: e.target.value})}
                  placeholder="https://hooks.slack.com/services/..."
                  className="w-full px-4 py-2 bg-gray-800/50 border border-gray-700 rounded-lg text-white placeholder-gray-600 focus:outline-none focus:border-cyan-500"
                />
              </div>
            </>
          )}
        </div>
      </div>

      {/* Geo-blocking */}
      <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-xl overflow-hidden">
        <div className="p-4 border-b border-cyan-500/20 flex items-center gap-3">
          <Globe className="w-5 h-5 text-cyan-400" />
          <h3 className="text-lg font-semibold text-white">Geo-blocking</h3>
        </div>
        <div className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-white font-medium">Enable Geo-blocking</p>
              <p className="text-sm text-gray-500">Block connections from specific countries</p>
            </div>
            <button
              onClick={() => setSettings({...settings, geoBlocking: !settings.geoBlocking})}
              className={`w-14 h-8 rounded-full transition-colors ${settings.geoBlocking ? 'bg-cyan-500' : 'bg-gray-700'}`}
            >
              <span className={`block w-6 h-6 bg-white rounded-full shadow transform transition-transform ${settings.geoBlocking ? 'translate-x-7' : 'translate-x-1'}`}></span>
            </button>
          </div>
        </div>
      </div>

      {/* Save Button */}
      <div className="flex justify-end">
        <button className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-cyan-500 to-purple-600 text-white font-medium rounded-lg hover:opacity-90 transition-opacity">
          <Save className="w-5 h-5" />
          Save Settings
        </button>
      </div>
    </div>
  )
}
