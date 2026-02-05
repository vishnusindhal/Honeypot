import json
import uuid
from datetime import datetime

class HoneypotLogger:
    def __init__(self, log_file="honeypot_audit.json"):
        self.log_file = log_file

    def log_command(self, session_id, source_ip, username, command_str, 
                    cwd, skill_level="Low", intent="Unknown", 
                    severity="Low", response_type="success"):
        
        entry = {
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "session_id": session_id,
            "source_ip": source_ip,
            "username": username,
            "tty": "pts/0",
            "command": {
                "raw_input": command_str,
                "normalized": command_str.strip(),
                "category": self._categorize_command(command_str)
            },
            "system_context": {
                "cwd": cwd,
                "privilege_level": "root" if username == "root" else "user",
                "environment_snapshot": "hash_placeholder" 
            },
            "behavior_analysis": {
                "intent": intent,
                "skill_level": skill_level,
                "confidence_score": 0.85
            },
            "threat_assessment": {
                "severity": severity,
                "tactic": "Discovery", # logical default, can be dynamic
                "technique": "T1059"   # Command and Scripting Interpreter
            },
            "response_metadata": {
                "response_type": response_type,
                "deception_depth": 1,
                "response_delay_ms": 500
            }
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def _categorize_command(self, cmd):
        cmd = cmd.strip().split()[0] if cmd.strip() else ""
        recon = ["ls", "whoami", "id", "groups", "uname", "pwd", "cat"]
        priv_esc = ["sudo", "su", "chmod"]
        persistence = ["crontab", "systemctl"]
        net = ["wget", "curl", "netstat", "ss"]
        
        if cmd in recon: return "Recon"
        if cmd in priv_esc: return "PrivEsc"
        if cmd in persistence: return "Persistence"
        if cmd in net: return "Exfiltration/Network"
        return "Unknown"
