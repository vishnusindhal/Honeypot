import uuid
from datetime import datetime
from database import get_db


class HoneypotLogger:
    def __init__(self):
        self.db = get_db()

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
                "tactic": "Discovery",
                "technique": "T1059"
            },
            "response_metadata": {
                "response_type": response_type,
                "deception_depth": 1,
                "response_delay_ms": 500
            }
        }

        try:
            self.db.commands.insert_one(entry)
        except Exception as e:
            print(f"[Logger] MongoDB write error: {e}")

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
