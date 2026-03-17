import json
import os
from datetime import datetime
from database import get_db


class SessionRecorder:
    """Records entire SSH sessions for analysis and replay."""

    def __init__(self, session_id, client_ip, username, recordings_dir="session_recordings"):
        self.session_id = session_id
        self.client_ip = client_ip
        self.username = username
        self.start_time = datetime.utcnow()
        self.end_time = None
        self.recordings_dir = recordings_dir
        self.transcript = []
        self.command_count = 0
        self.skill_progression = []
        self.db = get_db()

        # Ensure recordings directory exists (for text transcript backup)
        os.makedirs(recordings_dir, exist_ok=True)
        
        # Save initial "Active" state to MongoDB so it appears live on Dashboard
        self._save_to_mongodb()

    def record_interaction(self, command, output, skill_level, intent, cwd):
        """Record a single command/output interaction."""
        self.command_count += 1
        interaction = {
            "sequence": self.command_count,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "cwd": cwd,
            "command": command,
            "output": output,
            "analysis": {
                "skill_level": skill_level,
                "intent": intent
            }
        }
        self.transcript.append(interaction)
        self.skill_progression.append(skill_level)
        
        # Sync to MongoDB so dashboard gets live command counts and skill updates
        self._save_to_mongodb()

    def end_session(self):
        """Mark session as ended and save the recording."""
        self.end_time = datetime.utcnow()
        self._save_to_mongodb()
        self._save_text_transcript()  # Keep text backup

    def _save_to_mongodb(self):
        """Save session metadata and transcript to MongoDB."""
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0

        # --- Session metadata → sessions collection ---
        session_doc = {
            "session_id": self.session_id,
            "client_ip": self.client_ip,
            "username": self.username,
            "start_time": self.start_time.isoformat() + "Z",
            "end_time": self.end_time.isoformat() + "Z" if self.end_time else None,
            "duration_seconds": duration,
            "total_commands": self.command_count,
            "final_skill_level": self._determine_final_skill(),
            "skill_progression_summary": self._summarize_skill_progression(),
            "threat_summary": self._generate_threat_summary(),
            "last_command": self.transcript[-1]["command"] if self.transcript else ""
        }

        # --- Full transcript → session_replays collection ---
        replay_doc = {
            "session_id": self.session_id,
            "session_metadata": {
                "client_ip": self.client_ip,
                "username": self.username,
                "start_time": self.start_time.isoformat() + "Z",
                "end_time": self.end_time.isoformat() + "Z" if self.end_time else None,
                "duration_seconds": duration,
                "total_commands": self.command_count
            },
            "session_analysis": {
                "final_skill_level": self._determine_final_skill(),
                "skill_progression": self._summarize_skill_progression(),
                "threat_summary": self._generate_threat_summary()
            },
            "transcript": self.transcript
        }

        try:
            # Upsert so re-saving the same session doesn't fail
            self.db.sessions.update_one(
                {"session_id": self.session_id},
                {"$set": session_doc},
                upsert=True
            )
            self.db.session_replays.update_one(
                {"session_id": self.session_id},
                {"$set": replay_doc},
                upsert=True
            )
            print(f"[SessionRecorder] Saved session {self.session_id} to MongoDB")
        except Exception as e:
            print(f"[SessionRecorder] MongoDB write error: {e}")

    def _save_text_transcript(self):
        """Save human-readable text transcript as backup."""
        filepath = os.path.join(
            self.recordings_dir,
            f"{self.session_id}_{self.start_time.strftime('%Y%m%d_%H%M%S')}.txt"
        )

        lines = [
            "=" * 60,
            f"SESSION TRANSCRIPT",
            "=" * 60,
            f"Session ID: {self.session_id}",
            f"Client IP:  {self.client_ip}",
            f"Username:   {self.username}",
            f"Start:      {self.start_time.isoformat()}",
            f"End:        {self.end_time.isoformat() if self.end_time else 'Active'}",
            f"Commands:   {self.command_count}",
            "=" * 60,
            ""
        ]

        for interaction in self.transcript:
            lines.append(f"[{interaction['timestamp']}]")
            lines.append(f"{self.username}@prod-db-01:{interaction['cwd']}$ {interaction['command']}")
            if interaction['output']:
                lines.append(interaction['output'].rstrip())
            lines.append("")

        try:
            with open(filepath, "w") as f:
                f.write("\n".join(lines))
        except Exception as e:
            print(f"[SessionRecorder] Text transcript write error: {e}")

    def _determine_final_skill(self):
        """Determine the attacker's final skill level."""
        if not self.skill_progression:
            return "Unknown"

        counts = {"Low": 0, "Medium": 0, "High": 0}
        for skill in self.skill_progression:
            if skill in counts:
                counts[skill] += 1

        if counts["High"] > 0:
            return "High"
        if counts["Medium"] > counts["Low"]:
            return "Medium"
        return "Low"

    def _summarize_skill_progression(self):
        """Generate a summary of how skill evolved during session."""
        if len(self.skill_progression) < 2:
            return "Insufficient data"

        first_half = self.skill_progression[:len(self.skill_progression)//2]
        second_half = self.skill_progression[len(self.skill_progression)//2:]

        def avg_skill(skills):
            mapping = {"Low": 1, "Medium": 2, "High": 3}
            return sum(mapping.get(s, 1) for s in skills) / len(skills) if skills else 1

        first_avg = avg_skill(first_half)
        second_avg = avg_skill(second_half)

        if second_avg > first_avg + 0.3:
            return "Escalating - attacker became more sophisticated"
        elif second_avg < first_avg - 0.3:
            return "De-escalating - attacker simplified approach"
        return "Stable - consistent skill level throughout"

    def _generate_threat_summary(self):
        """Generate a threat intelligence summary."""
        categories = {"Recon": 0, "PrivEsc": 0, "Persistence": 0, "Network": 0, "Other": 0}

        for interaction in self.transcript:
            intent = interaction["analysis"]["intent"]
            if "Recon" in intent:
                categories["Recon"] += 1
            elif "Privilege" in intent:
                categories["PrivEsc"] += 1
            elif "Persist" in intent:
                categories["Persistence"] += 1
            elif "Network" in intent or "Exfil" in intent:
                categories["Network"] += 1
            else:
                categories["Other"] += 1

        primary_activity = max(categories, key=categories.get)

        return {
            "primary_activity": primary_activity,
            "activity_breakdown": categories,
            "recommendations": self._generate_recommendations(categories)
        }

    def _generate_recommendations(self, categories):
        """Generate security recommendations based on attacker behavior."""
        recs = []

        if categories["PrivEsc"] > 2:
            recs.append("ALERT: Multiple privilege escalation attempts detected")
        if categories["Persistence"] > 0:
            recs.append("ALERT: Attacker attempted to establish persistence")
        if categories["Network"] > 3:
            recs.append("ALERT: Significant network reconnaissance or exfiltration attempts")
        if categories["Recon"] > 10:
            recs.append("INFO: Extensive reconnaissance - likely automated scanning")

        if not recs:
            recs.append("INFO: Standard reconnaissance activity detected")

        return recs

    def get_live_summary(self):
        """Get a live summary of the current session (for monitoring)."""
        return {
            "session_id": self.session_id,
            "client_ip": self.client_ip,
            "username": self.username,
            "duration_seconds": (datetime.utcnow() - self.start_time).total_seconds(),
            "command_count": self.command_count,
            "current_skill_level": self.skill_progression[-1] if self.skill_progression else "Unknown",
            "last_command": self.transcript[-1]["command"] if self.transcript else None
        }


class SessionReplay:
    """Replays recorded sessions from MongoDB."""

    def __init__(self, session_id):
        db = get_db()
        self.recording = db.session_replays.find_one(
            {"session_id": session_id},
            {"_id": 0}
        )
        if not self.recording:
            raise ValueError(f"Session {session_id} not found in database")

    def get_metadata(self):
        return self.recording["session_metadata"]

    def get_analysis(self):
        return self.recording["session_analysis"]

    def get_transcript(self):
        return self.recording["transcript"]

    def print_transcript(self):
        """Print the session transcript to console."""
        meta = self.recording["session_metadata"]
        print("=" * 60)
        print(f"Session: {meta.get('session_id', self.recording.get('session_id', 'unknown'))}")
        print(f"From: {meta['client_ip']} as {meta['username']}")
        print(f"Duration: {meta['duration_seconds']:.1f}s ({meta['total_commands']} commands)")
        print("=" * 60)

        for entry in self.recording["transcript"]:
            print(f"\n[{entry['sequence']}] {meta['username']}@prod-db-01:{entry['cwd']}$ {entry['command']}")
            if entry['output']:
                print(entry['output'][:500])

    def search_commands(self, pattern):
        """Search for commands matching a pattern."""
        matches = []
        for entry in self.recording["transcript"]:
            if pattern.lower() in entry["command"].lower():
                matches.append(entry)
        return matches

    def get_commands_by_intent(self, intent):
        """Filter commands by intent category."""
        return [e for e in self.recording["transcript"] if intent.lower() in e["analysis"]["intent"].lower()]
