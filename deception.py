import random
import time

class DeceptionEngine:
    """
    Advanced Deception Engine with:
    - Skill level detection
    - Adaptive response delays
    - Selective secret leaking
    - Fake vulnerability injection
    """
    
    def __init__(self):
        self.command_history = []
        self.skill_level = "Low"
        self.intent = "Unknown"
        self.score = 0
        self.secrets_leaked = []
        self.vulnerabilities_shown = []
        
        # Decoy secrets to leak progressively
        self.decoy_secrets = [
            {"trigger_score": 5, "type": "env_hint", "content": "Check .env files for credentials"},
            {"trigger_score": 10, "type": "db_cred", "content": "mysql -u db_admin -p'Pr0d_S3cur3_2024!'"},
            {"trigger_score": 15, "type": "api_key", "content": "AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE"},
            {"trigger_score": 25, "type": "ssh_key", "content": "Found backup SSH key in /var/backups/.ssh_backup/"},
        ]
        
        # Fake vulnerabilities to show to advanced attackers
        self.fake_vulnerabilities = [
            {"trigger_skill": "Medium", "vuln": "sudo_version", "details": "sudo 1.8.23 - CVE-2019-14287 (not actually exploitable here)"},
            {"trigger_skill": "High", "vuln": "kernel", "details": "Linux 5.4.0-150 - Potential DirtyPipe variant (honeypot bait)"},
            {"trigger_skill": "High", "vuln": "mysql_udf", "details": "MySQL UDF plugin directory writable (fake)"},
        ]

    def analyze(self, cmd_str):
        """Analyze command and return skill level + intent."""
        self.command_history.append(cmd_str)
        self._update_score(cmd_str)
        self._derive_intent(cmd_str)
        return self.skill_level, self.intent

    def get_response_delay(self):
        """
        Get adaptive response delay based on attacker skill.
        - Low skill: Faster responses (they expect instant)
        - High skill: Realistic delays (they notice if too fast)
        """
        if self.skill_level == "Low":
            return random.uniform(0.1, 0.3)
        elif self.skill_level == "Medium":
            return random.uniform(0.2, 0.5)
        else:  # High
            return random.uniform(0.3, 1.0)

    def should_leak_secret(self):
        """
        Determine if we should leak a decoy secret.
        Returns the secret to leak or None.
        """
        for secret in self.decoy_secrets:
            if secret["trigger_score"] <= self.score and secret["type"] not in self.secrets_leaked:
                self.secrets_leaked.append(secret["type"])
                return secret
        return None

    def get_fake_vulnerability(self):
        """
        Get a fake vulnerability hint to bait advanced attackers.
        Returns vulnerability details or None.
        """
        for vuln in self.fake_vulnerabilities:
            if vuln["trigger_skill"] == self.skill_level and vuln["vuln"] not in self.vulnerabilities_shown:
                self.vulnerabilities_shown.append(vuln["vuln"])
                return vuln
        return None

    def inject_breadcrumb(self, cmd_str):
        """
        Inject breadcrumbs into command output to guide attackers.
        Returns additional output to append or None.
        """
        # Only inject for medium+ skill attackers
        if self.skill_level == "Low":
            return None
        
        # Check for specific commands where we can inject hints
        if "find" in cmd_str and ".env" in cmd_str:
            secret = self.should_leak_secret()
            if secret and secret["type"] == "env_hint":
                return "\n# Note: Production .env contains AWS credentials\n"
        
        if "cat" in cmd_str and "history" in cmd_str:
            if self.score > 10:
                return "# Old command from admin: mysql -u root -pOldPassword123\n"
        
        if "sudo -l" in cmd_str and self.skill_level == "High":
            vuln = self.get_fake_vulnerability()
            if vuln:
                return f"\n# Note: {vuln['details']}\n"
        
        return None

    def _update_score(self, cmd):
        """Update skill score based on command sophistication."""
        # Command weightings
        high_tier = [
            "unset", "export", "nohup", "insmod", "rmmod", "chattr", 
            "nc", "socat", "python", "perl", "ruby", "base64", "xxd",
            "iptables", "tcpdump", "strace", "ltrace"
        ]
        med_tier = [
            "wget", "curl", "sudo", "su", "chmod", "chown", 
            "ps", "netstat", "ss", "systemctl", "crontab", "find",
            "grep", "history", "env", "top", "crontab"
        ]
        low_tier = ["ls", "pwd", "whoami", "id", "cat", "echo", "cd", "clear"]
        
        normalized = cmd.split()[0] if cmd.strip() else ""
        
        # Score based on command
        if normalized in high_tier:
            self.score += 5
        elif normalized in med_tier:
            self.score += 2
        elif normalized in low_tier:
            self.score += 0.5
        
        # Bonus for sophisticated patterns
        if "|" in cmd:  # Piping
            self.score += 1
        if ">" in cmd or ">>" in cmd:  # Redirection
            self.score += 1
        if "$(" in cmd or "`" in cmd:  # Command substitution
            self.score += 2
        if "&&" in cmd or "||" in cmd:  # Chaining
            self.score += 1
        if "/dev/null" in cmd:  # Hiding output
            self.score += 2
        if "2>&1" in cmd:  # Stderr redirection
            self.score += 1
            
        # Determine Level
        if self.score > 20:
            self.skill_level = "High"
        elif self.score > 5:
            self.skill_level = "Medium"
        else:
            self.skill_level = "Low"

    def _derive_intent(self, cmd):
        """Determine the intent behind a command."""
        normalized = cmd.split()[0] if cmd.strip() else ""
        full_cmd = cmd.lower()
        
        # Categorization
        recon = ["ls", "dir", "whoami", "id", "pwd", "uname", "cat", "find", "grep", "tree", "file", "head", "tail"]
        privesc = ["sudo", "su", "chmod", "pkexec"]
        persistence = ["crontab", "systemctl", "rc.local", "authorized_keys", "bashrc"]
        exfil = ["wget", "curl", "nc", "netstat", "ss", "scp", "ftp", "rsync"]
        cleanup = ["unset", "history", "rm", "shred"]
        
        # Check for specific patterns
        if any(p in full_cmd for p in ["shadow", "passwd", "password", "credential", "secret", "key"]):
            self.intent = "Credential Harvesting"
        elif any(p in full_cmd for p in ["/etc/cron", "authorized_keys", ".bashrc", ".profile"]):
            self.intent = "Persistence"
        elif normalized in recon:
            self.intent = "Reconnaissance"
        elif normalized in privesc:
            self.intent = "Privilege Escalation"
        elif normalized in persistence:
            self.intent = "Persistence"
        elif normalized in exfil:
            self.intent = "Exfiltration/Network"
        elif normalized in cleanup:
            self.intent = "Anti-Forensics"
        else:
            self.intent = "Command Execution"

    def get_session_profile(self):
        """Generate a profile of the attacker based on behavior."""
        return {
            "skill_level": self.skill_level,
            "score": self.score,
            "total_commands": len(self.command_history),
            "secrets_leaked": self.secrets_leaked,
            "vulnerabilities_shown": self.vulnerabilities_shown,
            "behavior_summary": self._generate_behavior_summary()
        }

    def _generate_behavior_summary(self):
        """Generate a summary of attacker behavior patterns."""
        patterns = []
        
        history_str = " ".join(self.command_history).lower()
        
        if any(p in history_str for p in ["shadow", "passwd", "env", "credential"]):
            patterns.append("Credential hunting")
        if any(p in history_str for p in ["sudo", "su ", "chmod +s"]):
            patterns.append("Privilege escalation attempts")
        if any(p in history_str for p in ["crontab", "authorized_keys", "systemctl enable"]):
            patterns.append("Persistence attempts")
        if any(p in history_str for p in ["wget", "curl", "nc ", "netcat"]):
            patterns.append("Data exfiltration or tool download")
        if any(p in history_str for p in ["unset", "history -c", "rm -rf"]):
            patterns.append("Anti-forensics activity")
        if any(p in history_str for p in ["uname", "kernel", "dmesg"]):
            patterns.append("Kernel/system enumeration")
        
        return patterns if patterns else ["Standard reconnaissance"]
