import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Area, AreaChart
} from 'recharts'

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-gray-900 border border-cyan-500/30 rounded-lg p-3 shadow-xl">
        <p className="text-white font-medium">{label}</p>
        <p className="text-cyan-400">{payload[0].value}</p>
      </div>
    )
  }
  return null
}

export function CommandBarChart({ data }) {
  return (
    <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Command Frequency</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <XAxis 
            dataKey="name" 
            stroke="#6b7280" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis 
            stroke="#6b7280" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="count" 
            fill="url(#barGradient)" 
            radius={[4, 4, 0, 0]}
          />
          <defs>
            <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#22d3ee" />
              <stop offset="100%" stopColor="#8b5cf6" />
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function RiskDonutChart({ data }) {
  return (
    <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Risk Distribution</h3>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={90}
            paddingAngle={5}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
        </PieChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap justify-center gap-4 mt-4">
        {data.map((item, index) => (
          <div key={index} className="flex items-center gap-2">
            <span 
              className="w-3 h-3 rounded-full" 
              style={{ backgroundColor: item.color }}
            ></span>
            <span className="text-sm text-gray-400">{item.name}</span>
            <span className="text-sm text-white font-medium">{item.value}%</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export function TimelineChart({ data }) {
  return (
    <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Commands Over Time</h3>
      <ResponsiveContainer width="100%" height={250}>
        <AreaChart data={data}>
          <defs>
            <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.3} />
              <stop offset="100%" stopColor="#22d3ee" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis 
            dataKey="time" 
            stroke="#6b7280" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis 
            stroke="#6b7280" 
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area 
            type="monotone" 
            dataKey="commands" 
            stroke="#22d3ee" 
            strokeWidth={2}
            fill="url(#areaGradient)" 
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

export function SkillHeatmap({ data }) {
  return (
    <div className="bg-gray-900/60 backdrop-blur-xl border border-cyan-500/20 rounded-2xl p-6">
      <h3 className="text-lg font-semibold text-white mb-4">Skill Level Distribution</h3>
      <div className="space-y-4">
        {data.map((item, index) => (
          <div key={index}>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-400">{item.name}</span>
              <span className="text-white font-medium">{item.value}%</span>
            </div>
            <div className="h-3 bg-gray-800 rounded-full overflow-hidden">
              <div 
                className="h-full rounded-full transition-all duration-1000"
                style={{ 
                  width: `${item.value}%`,
                  backgroundColor: item.color
                }}
              ></div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
